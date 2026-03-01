from typing import Dict, List, Callable, Any, Optional, Union

from ..telegram_types import Message, CallbackQuery  # Zmienione
from ..exceptions import SkipHandler
from .context import Context

class Router:
    def __init__(self, name: str = "main"):
        self.name = name
        self.message_handlers: List[Dict[str, Any]] = []
        self.callback_handlers: List[Dict[str, Any]] = []
        self.routers: List['Router'] = []

    def message(self, *filters):
        """Dekorator dla handlerów wiadomości"""

        def decorator(func: Callable):
            self.message_handlers.append({
                'func': func,
                'filters': filters
            })
            return func

        return decorator

    def callback(self, *filters):
        """Dekorator dla handlerów callback query"""

        def decorator(func: Callable):
            self.callback_handlers.append({
                'func': func,
                'filters': filters
            })
            return func

        return decorator

    def include_router(self, router: 'Router'):
        """Dołącz pod-router"""
        self.routers.append(router)

    async def process_message(
            self,
            context: Context,
            state: Optional['FSMContext'] = None
    ) -> bool:
        """Przetwórz wiadomość przez wszystkie handlery"""

        # Sprawdź pod-routery
        for router in self.routers:
            if await router.process_message(context, state):
                return True

        # Sprawdź handlery
        for handler in self.message_handlers:
            try:
                if await self._check_filters(handler['filters'], context.message, state):
                    await handler['func'](context)
                    return True
            except SkipHandler:
                continue

        return False

    async def process_callback(
            self,
            context: Context,
            state: Optional['FSMContext'] = None
    ) -> bool:
        """Przetwórz callback query"""

        # Sprawdź pod-routery
        for router in self.routers:
            if await router.process_callback(context, state):
                return True

        # Sprawdź handlery
        for handler in self.callback_handlers:
            try:
                if await self._check_filters(handler['filters'], context.callback_query, state):
                    await handler['func'](context)
                    return True
            except SkipHandler:
                continue

        return False

    async def _check_filters(
            self,
            filters: tuple,
            obj: Any,
            state: Optional['FSMContext'] = None
    ) -> bool:
        """Sprawdź czy obiekt przechodzi przez filtry"""

        current_state = await state.get_state() if state else None

        for f in filters:
            if hasattr(f, '_state_filter'):
                required = f._state_filter
                if hasattr(required, 'name'):
                    required = required.name
                if required != current_state:
                    return False
            elif callable(f):
                if hasattr(f, '__call__') and inspect.iscoroutinefunction(f):
                    if not await f(obj):
                        return False
                elif not f(obj):
                    return False

        return True