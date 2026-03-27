# middleware/base.py
"""
Middleware system for telegram_async
"""
from typing import Callable, Dict, Any, Optional, Awaitable, List
import logging
import time
from ..telegram_types import Update
from ..dispatcher.context import Context
from ..exceptions import MiddlewareError, SkipHandler, CancelHandler

# Type for middleware handler
MiddlewareHandler = Callable[[Update, Dict[str, Any]], Awaitable[Any]]


class BaseMiddleware:
    """
    Base class for middleware

    Example:
        class LoggingMiddleware(BaseMiddleware):
            async def __call__(self, handler, event, data):
                logger.info(f"Processing update {event.update_id}")
                result = await handler(event, data)
                logger.info(f"Update processed")
                return result
    """

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__

    async def __call__(
            self,
            handler: MiddlewareHandler,
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        """
        Main middleware method

        Args:
            handler: Next handler/middleware to call
            event: Received update from Telegram
            data: Dictionary with data (bot, dispatcher, fsm, etc.)

        Returns:
            Result of the handler execution
        """
        return await handler(event, data)

    def __repr__(self) -> str:
        return f"<{self.name}>"


class MiddlewareManager:
    """
    Middleware manager - stores and executes middleware in a chain
    """

    def __init__(self):
        self.middlewares: List[BaseMiddleware] = []
        self.logger = logging.getLogger(__name__)

    def add(self, middleware: BaseMiddleware):
        """Adds middleware to the collection"""
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError(f"Expected BaseMiddleware, got {type(middleware)}")
        self.middlewares.append(middleware)
        self.logger.debug(f"Added middleware: {middleware}")

    def remove(self, middleware_name: str) -> bool:
        """Removes middleware by name"""
        for i, m in enumerate(self.middlewares):
            if m.name == middleware_name:
                self.middlewares.pop(i)
                self.logger.debug(f"Removed middleware: {m}")
                return True
        return False

    def clear(self):
        """Clears all middlewares"""
        self.middlewares.clear()
        self.logger.debug("Cleared all middlewares")

    async def run(
            self,
            event: Update,
            data: Dict[str, Any],
            final_handler: MiddlewareHandler
    ) -> Any:
        """
        Runs the middleware chain

        Args:
            event: Update to process
            data: Contextual data
            final_handler: Final handler to call

        Returns:
            Result of processing
        """
        index = 0
        middlewares = self.middlewares.copy()

        async def next_middleware() -> Any:
            nonlocal index
            if index < len(middlewares):
                current = middlewares[index]
                index += 1
                try:
                    return await current(next_middleware, event, data)
                except SkipHandler:
                    # Skip current handler, go to next
                    self.logger.debug(f"Skipped handler in {current}")
                    return await next_middleware()
                except CancelHandler:
                    # Cancel entire processing
                    self.logger.debug(f"Cancelled processing in {current}")
                    return None
                except Exception as e:
                    raise MiddlewareError(f"Error in {current}: {e}", current.name)
            else:
                return await final_handler(event, data)

        return await next_middleware()


# Concrete middleware implementations

class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging updates"""

    def __init__(self, logger: Optional[logging.Logger] = None):
        super().__init__("LoggingMiddleware")
        self.logger = logger or logging.getLogger(__name__)

    async def __call__(self, handler, event, data):
        self.logger.info(f"📩 Processing update {event.update_id}")
        start_time = time.time()

        try:
            result = await handler(event, data)
            duration = (time.time() - start_time) * 1000
            self.logger.info(f"✅ Update {event.update_id} processed in {duration:.2f}ms")
            return result
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            self.logger.error(f"❌ Error processing update {event.update_id}: {e} ({duration:.2f}ms)")
            raise


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware for rate limiting requests"""

    def __init__(self, rate: int = 5, per: int = 10):
        """
        Args:
            rate: Maximum number of requests
            per: Within how many seconds
        """
        super().__init__("ThrottlingMiddleware")
        self.rate = rate
        self.per = per
        self.users = {}
        self.logger = logging.getLogger(__name__)

    async def __call__(self, handler, event, data):
        # Get user_id from event
        user_id = None
        if event.message and event.message.from_user:
            user_id = event.message.from_user.id
        elif event.callback_query and event.callback_query.from_user:
            user_id = event.callback_query.from_user.id
        elif event.inline_query and event.inline_query.from_user:
            user_id = event.inline_query.from_user.id

        if user_id:
            if not await self._check_rate_limit(user_id):
                self.logger.warning(f"Rate limit exceeded for user {user_id}")
                # Limit exceeded - notification could be sent here
                return None  # Skip further processing

        return await handler(event, data)

    async def _check_rate_limit(self, user_id: int) -> bool:
        now = time.time()
        user_data = self.users.get(user_id, [])

        # Remove old entries
        user_data = [t for t in user_data if now - t < self.per]

        if len(user_data) >= self.rate:
            self.users[user_id] = user_data
            return False

        user_data.append(now)
        self.users[user_id] = user_data
        return True


class RoleMiddleware(BaseMiddleware):
    """Middleware for checking user roles"""

    def __init__(self, role_manager):
        """
        Args:
            role_manager: Role manager (from roles.py)
        """
        super().__init__("RoleMiddleware")
        self.role_manager = role_manager

    async def __call__(self, handler, event, data):
        # Get user_id
        user_id = None
        if event.message and event.message.from_user:
            user_id = event.message.from_user.id
        elif event.callback_query and event.callback_query.from_user:
            user_id = event.callback_query.from_user.id

        if user_id:
            # Add role to data
            data['user_role'] = self.role_manager.get_role(user_id)

        return await handler(event, data)


class FSMContextMiddleware(BaseMiddleware):
    """Middleware for injecting FSM context into data"""

    def __init__(self):
        super().__init__("FSMContextMiddleware")

    async def __call__(self, handler, event, data):
        # FSM context is already added in the dispatcher
        # This middleware can extend FSM functionality
        return await handler(event, data)


class MetricsMiddleware(BaseMiddleware):
    """Middleware for collecting metrics"""

    def __init__(self):
        super().__init__("MetricsMiddleware")
        self.metrics = {
            'total_updates': 0,
            'updates_by_type': {},
            'errors': 0,
            'processing_times': []
        }

    async def __call__(self, handler, event, data):
        self.metrics['total_updates'] += 1

        # Count update types
        update_type = self._get_update_type(event)
        self.metrics['updates_by_type'][update_type] = \
            self.metrics['updates_by_type'].get(update_type, 0) + 1

        start_time = time.time()
        try:
            result = await handler(event, data)
            processing_time = time.time() - start_time
            self.metrics['processing_times'].append(processing_time)
            # Keep only last 1000 times
            if len(self.metrics['processing_times']) > 1000:
                self.metrics['processing_times'] = self.metrics['processing_times'][-1000:]
            return result
        except Exception:
            self.metrics['errors'] += 1
            raise

    def _get_update_type(self, event: Update) -> str:
        if event.message:
            return 'message'
        elif event.callback_query:
            return 'callback_query'
        elif event.inline_query:
            return 'inline_query'
        elif event.edited_message:
            return 'edited_message'
        else:
            return 'other'

    def get_stats(self) -> Dict:
        """Returns statistics"""
        avg_time = sum(self.metrics['processing_times']) / len(self.metrics['processing_times']) \
            if self.metrics['processing_times'] else 0
        return {
            'total_updates': self.metrics['total_updates'],
            'updates_by_type': self.metrics['updates_by_type'],
            'errors': self.metrics['errors'],
            'avg_processing_time_ms': avg_time * 1000
        }


class ErrorHandlingMiddleware(BaseMiddleware):
    """Middleware for global error handling"""

    def __init__(self, error_handler: Optional[Callable] = None):
        super().__init__("ErrorHandlingMiddleware")
        self.error_handler = error_handler

    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            if self.error_handler:
                # Pass error to error handler
                await self.error_handler(event, e, data)
            else:
                # Default handling - log error
                logging.error(f"Unhandled error in update {event.update_id}: {e}")
            raise


# Decorator for creating middleware from a function
def middleware(func: Callable) -> BaseMiddleware:
    """
    Decorator converting a function into middleware

    Example:
        @middleware
        async def my_middleware(handler, event, data):
            print("Before handler")
            result = await handler(event, data)
            print("After handler")
            return result
    """

    class FunctionMiddleware(BaseMiddleware):
        def __init__(self, f):
            super().__init__(f.__name__)
            self.func = f

        async def __call__(self, handler, event, data):
            return await self.func(handler, event, data)

    return FunctionMiddleware(func)
