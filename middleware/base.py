# middleware/base.py
"""
System middleware dla telegram_async
"""
from typing import Callable, Dict, Any, Optional, Awaitable
import logging
import time
from functools import wraps
from ..types import Update
from ..context import Context
from ..exceptions import MiddlewareError, SkipHandler, CancelHandler

# Typ dla handlera middleware
MiddlewareHandler = Callable[[Update, Dict[str, Any]], Awaitable[Any]]


class BaseMiddleware:
    """
    Bazowa klasa dla middleware

    Przykład:
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
        Główna metoda middleware

        Args:
            handler: Następny handler/middleware do wywołania
            event: Otrzymany update z Telegram
            data: Słownik z danymi (bot, dispatcher, fsm, itp.)

        Returns:
            Wynik wykonania handlera
        """
        return await handler(event, data)

    def __repr__(self) -> str:
        return f"<{self.name}>"


class MiddlewareManager:
    """
    Zarządca middleware - przechowuje i wykonuje middleware w łańcuchu
    """

    def __init__(self):
        self.middlewares: list[BaseMiddleware] = []
        self.logger = logging.getLogger(__name__)

    def add(self, middleware: BaseMiddleware):
        """Dodaje middleware do kolekcji"""
        if not isinstance(middleware, BaseMiddleware):
            raise TypeError(f"Expected BaseMiddleware, got {type(middleware)}")
        self.middlewares.append(middleware)
        self.logger.debug(f"Added middleware: {middleware}")

    def remove(self, middleware_name: str) -> bool:
        """Usuwa middleware po nazwie"""
        for i, m in enumerate(self.middlewares):
            if m.name == middleware_name:
                self.middlewares.pop(i)
                self.logger.debug(f"Removed middleware: {m}")
                return True
        return False

    def clear(self):
        """Czyści wszystkie middleware"""
        self.middlewares.clear()
        self.logger.debug("Cleared all middlewares")

    async def run(
            self,
            event: Update,
            data: Dict[str, Any],
            final_handler: MiddlewareHandler
    ) -> Any:
        """
        Uruchamia łańcuch middleware

        Args:
            event: Update do przetworzenia
            data: Dane kontekstowe
            final_handler: Ostateczny handler do wywołania

        Returns:
            Wynik przetwarzania
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
                    # Pomija bieżący handler, przechodzi do następnego
                    self.logger.debug(f"Skipped handler in {current}")
                    return await next_middleware()
                except CancelHandler:
                    # Anuluje całe przetwarzanie
                    self.logger.debug(f"Cancelled processing in {current}")
                    return None
                except Exception as e:
                    raise MiddlewareError(f"Error in {current}: {e}", current.name)
            else:
                return await final_handler(event, data)

        return await next_middleware()


# Konkretne implementacje middleware

class LoggingMiddleware(BaseMiddleware):
    """Middleware do logowania update'ów"""

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
    """Middleware do ograniczania częstotliwości zapytań"""

    def __init__(self, rate: int = 5, per: int = 10):
        """
        Args:
            rate: Maksymalna liczba zapytań
            per: W ciągu ilu sekund
        """
        super().__init__("ThrottlingMiddleware")
        self.rate = rate
        self.per = per
        self.users = {}
        self.logger = logging.getLogger(__name__)

    async def __call__(self, handler, event, data):
        # Pobierz user_id z eventu
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
                # Przekroczono limit - można wysłać powiadomienie
                if event.message and event.message.chat:
                    # Opcjonalnie: wyślij powiadomienie o limicie
                    pass
                return None  # Pomija dalsze przetwarzanie

        return await handler(event, data)

    async def _check_rate_limit(self, user_id: int) -> bool:
        now = time.time()
        user_data = self.users.get(user_id, [])

        # Usuń stare wpisy
        user_data = [t for t in user_data if now - t < self.per]

        if len(user_data) >= self.rate:
            self.users[user_id] = user_data
            return False

        user_data.append(now)
        self.users[user_id] = user_data
        return True


class RoleMiddleware(BaseMiddleware):
    """Middleware do sprawdzania ról użytkowników"""

    def __init__(self, role_manager):
        """
        Args:
            role_manager: Manager ról (z roles.py)
        """
        super().__init__("RoleMiddleware")
        self.role_manager = role_manager

    async def __call__(self, handler, event, data):
        # Pobierz user_id
        user_id = None
        if event.message and event.message.from_user:
            user_id = event.message.from_user.id
        elif event.callback_query and event.callback_query.from_user:
            user_id = event.callback_query.from_user.id

        if user_id:
            # Dodaj rolę do danych
            data['user_role'] = self.role_manager.get_role(user_id)

        return await handler(event, data)


class FSMContextMiddleware(BaseMiddleware):
    """Middleware do wstrzykiwania FSM context do danych"""

    def __init__(self):
        super().__init__("FSMContextMiddleware")

    async def __call__(self, handler, event, data):
        # FSM context jest już dodawany w dispatcherze
        # Ten middleware może rozszerzać funkcjonalność FSM
        return await handler(event, data)


class MetricsMiddleware(BaseMiddleware):
    """Middleware do zbierania metryk"""

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

        # Zliczaj typy update'ów
        update_type = self._get_update_type(event)
        self.metrics['updates_by_type'][update_type] = \
            self.metrics['updates_by_type'].get(update_type, 0) + 1

        start_time = time.time()
        try:
            result = await handler(event, data)
            processing_time = time.time() - start_time
            self.metrics['processing_times'].append(processing_time)
            # Zachowaj tylko ostatnie 1000 czasów
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
        """Zwraca statystyki"""
        avg_time = sum(self.metrics['processing_times']) / len(self.metrics['processing_times']) \
            if self.metrics['processing_times'] else 0
        return {
            'total_updates': self.metrics['total_updates'],
            'updates_by_type': self.metrics['updates_by_type'],
            'errors': self.metrics['errors'],
            'avg_processing_time_ms': avg_time * 1000
        }


class ErrorHandlingMiddleware(BaseMiddleware):
    """Middleware do globalnej obsługi błędów"""

    def __init__(self, error_handler: Optional[Callable] = None):
        super().__init__("ErrorHandlingMiddleware")
        self.error_handler = error_handler

    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except Exception as e:
            if self.error_handler:
                # Przekaż błąd do handlera błędów
                await self.error_handler(event, e, data)
            else:
                # Domyślna obsługa - zaloguj błąd
                logging.error(f"Unhandled error in update {event.update_id}: {e}")
            raise


# Dekorator do tworzenia middleware z funkcji
def middleware(func: Callable) -> BaseMiddleware:
    """
    Dekorator zamieniający funkcję w middleware

    Przykład:
        @middleware
        async def my_middleware(handler, event, data):
            print("Before handler")
            result = await handler(event, data)
            print("After handler")
            return result
    """

    class FunctionMiddleware(BaseMiddleware):
        def __init__(self, func):
            super().__init__(func.__name__)
            self.func = func

        async def __call__(self, handler, event, data):
            return await self.func(handler, event, data)

    return FunctionMiddleware(func)