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
        # Custom context class injection
        self._context_class: Optional[type] = None

    def message(self, *filters, priority: int = 0):
        """
        Decorator for message handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['message'].append({
                'func': func,
                'filters': filters,
                'priority': priority
            })
            return func
        return decorator

    def callback_query(self, *filters, priority: int = 0):
        """
        Decorator for callback query handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['callback_query'].append({
                'func': func,
                'filters': filters,
                'priority': priority
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

    def shipping_query(self, *filters, priority: int = 0):
        """
        Decorator for shipping query handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['shipping_query'].append({
                'func': func,
                'filters': filters,
                'priority': priority
            })
            return func
        return decorator

    def pre_checkout_query(self, *filters, priority: int = 0):
        """
        Decorator for pre-checkout query handlers (payment validation)
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['pre_checkout_query'].append({
                'func': func,
                'filters': filters,
                'priority': priority
            })
            return func
        return decorator

    def successful_payment(self, *filters, priority: int = 0):
        """
        Decorator for successful payment handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            # Payment handlers work with message updates
            async def payment_filter(message: Message) -> bool:
                return hasattr(message, 'successful_payment') and message.successful_payment is not None

            self.handlers['message'].append({
                'func': func,
                'filters': (payment_filter,) + filters,
                'priority': priority
            })
            return func
        return decorator

    def poll(self, *filters, priority: int = 0):
        """
        Decorator for poll handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['poll'].append({
                'func': func,
                'filters': filters,
                'priority': priority
            })
            return func
        return decorator

    def poll_answer(self, *filters, priority: int = 0):
        """
        Decorator for poll answer handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['poll_answer'].append({
                'func': func,
                'filters': filters,
                'priority': priority
            })
            return func
        return decorator

    def chat_join_request(self, *filters, priority: int = 0):
        """
        Decorator for chat join request handlers
        
        Args:
            *filters: Filter functions
            priority: Handler priority (higher = executed first, default 0)
        """
        def decorator(func: Callable):
            self.handlers['chat_join_request'].append({
                'func': func,
                'filters': filters,
                'priority': priority
            })
            return func
        return decorator

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
        elif update.channel_post:
            update_type = 'channel_post'
            event = update.channel_post
        elif update.edited_channel_post:
            update_type = 'edited_channel_post'
            event = update.edited_channel_post
        elif update.inline_query:
            update_type = 'inline_query'
            event = update.inline_query
        elif update.chosen_inline_result:
            update_type = 'chosen_inline_result'
            event = update.chosen_inline_result
        elif update.shipping_query:
            update_type = 'shipping_query'
            event = update.shipping_query
        elif update.pre_checkout_query:
            update_type = 'pre_checkout_query'
            event = update.pre_checkout_query
        elif update.poll:
            update_type = 'poll'
            event = update.poll
        elif update.poll_answer:
            update_type = 'poll_answer'
            event = update.poll_answer
        elif update.my_chat_member:
            update_type = 'my_chat_member'
            event = update.my_chat_member
        elif update.chat_member:
            update_type = 'chat_member'
            event = update.chat_member
        elif update.chat_join_request:
            update_type = 'chat_join_request'
            event = update.chat_join_request
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

        # 2. Sort handlers by priority (higher first)
        sorted_handlers = sorted(
            self.handlers[update_type],
            key=lambda h: h.get('priority', 0),
            reverse=True
        )

        # 3. Process local handlers
        for handler_dict in sorted_handlers:
            try:
                if await self._check_filters(handler_dict['filters'], event, ctx):
                    # Use custom context class if set
                    handler_ctx = ctx
                    if self._context_class:
                        handler_ctx = self._context_class(
                            client=ctx.client,
                            update=ctx.update,
                            fsm=ctx.fsm
                        )
                    
                    await handler_dict['func'](handler_ctx)
                    return True
            except SkipHandler:
                continue
            except Exception as e:
                # Log error or re-raise
                raise e

        return False
    
    def set_context_class(self, context_class: type):
        """
        Set a custom context class for this router.
        
        Args:
            context_class: Custom Context subclass
        """
        self._context_class = context_class
