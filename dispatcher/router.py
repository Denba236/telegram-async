import inspect
from typing import Dict, List, Callable, Any, Optional, Union

from ..telegram_types import Message, CallbackQuery, Update
from ..exceptions import SkipHandler
from .context import Context

class Router:
    """
    Base router class for handling updates.
    Can be used to modularize bot logic by splitting handlers across multiple files.
    """

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.handlers: Dict[str, List[Dict[str, Any]]] = {
            'message': [],
            'callback_query': [],
            'edited_message': [],
            'channel_post': [],
            'edited_channel_post': [],
            'inline_query': [],
            'chosen_inline_result': [],
            'shipping_query': [],
            'pre_checkout_query': [],
            'poll': [],
            'poll_answer': [],
            'my_chat_member': [],
            'chat_member': [],
            'chat_join_request': [],
        }
        self.sub_routers: List['Router'] = []
        # Router-level middleware can be added here in the future
        self.middlewares: List[Callable] = []

    def message(self, *filters):
        """Decorator for message handlers"""
        def decorator(func: Callable):
            self.handlers['message'].append({
                'func': func,
                'filters': filters
            })
            return func
        return decorator

    def callback_query(self, *filters):
        """Decorator for callback query handlers"""
        def decorator(func: Callable):
            self.handlers['callback_query'].append({
                'func': func,
                'filters': filters
            })
            return func
        return decorator

    def command(self, command: str):
        """Decorator for command handlers (e.g. /start)"""
        def decorator(func: Callable):
            # Commands are specialized message handlers
            async def command_filter(message: Message) -> bool:
                if not message.text:
                    return False
                parts = message.text.split()
                if not parts:
                    return False
                return parts[0][1:].lower() == command.lower()

            self.handlers['message'].append({
                'func': func,
                'filters': (command_filter,)
            })
            return func
        return decorator

    def include_router(self, router: 'Router'):
        """Include a sub-router"""
        if router is self:
            raise ValueError("Cannot include router into itself")
        self.sub_routers.append(router)

    async def _check_filters(self, filters: tuple, event: Any, ctx: Context) -> bool:
        """Check if the event passes all filters"""
        current_state = await ctx.fsm.get_state() if ctx.fsm else None

        for f in filters:
            # State filter support
            if hasattr(f, '_state_filter'):
                required = f._state_filter
                if hasattr(required, 'name'):  # State object
                    required = required.name
                
                if required != current_state:
                    return False
            
            # Function/Coroutine filters
            elif inspect.iscoroutinefunction(f):
                if not await f(event):
                    return False
            elif callable(f):
                if not f(event):
                    return False
        return True

    async def feed_update(self, ctx: Context) -> bool:
        """
        Feed update to handlers and sub-routers.
        Returns True if the update was handled.
        """
        update = ctx.update
        
        # Determine update type
        update_type = None
        event = None
        
        if update.message:
            update_type = 'message'
            event = update.message
        elif update.callback_query:
            update_type = 'callback_query'
            event = update.callback_query
        elif update.edited_message:
            update_type = 'edited_message'
            event = update.edited_message
        # ... other types can be added here
        
        if not update_type or update_type not in self.handlers:
            # Try sub-routers even if we don't recognize the type locally
            for router in self.sub_routers:
                if await router.feed_update(ctx):
                    return True
            return False

        # 1. Process sub-routers first (depth-first)
        for router in self.sub_routers:
            if await router.feed_update(ctx):
                return True

        # 2. Process local handlers
        for handler_dict in self.handlers[update_type]:
            try:
                if await self._check_filters(handler_dict['filters'], event, ctx):
                    await handler_dict['func'](ctx)
                    return True
            except SkipHandler:
                continue
            except Exception as e:
                # Log error or re-raise
                raise e

        return False
