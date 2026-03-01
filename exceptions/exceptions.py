"""
System obsługi błędów dla telegram_async
"""
from typing import Optional, Dict


class TelegramError(Exception):
    """Bazowa klasa dla wszystkich błędów Telegram"""
    pass


class TelegramAPIError(TelegramError):
    """Błąd zwrócony przez Telegram API"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}" if code else message)


class NetworkError(TelegramError):
    """Błąd połączenia sieciowego"""

    def __init__(self, message: str = "Network connection failed"):
        self.message = message
        super().__init__(message)


class RateLimitError(TelegramAPIError):
    """Przekroczono limit zapytań (429 Too Many Requests)"""

    def __init__(self, retry_after: int, message: str = "Too Many Requests"):
        self.retry_after = retry_after
        super().__init__(message, 429)


class ForbiddenError(TelegramAPIError):
    """Bot został zablokowany lub nie ma uprawnień (403 Forbidden)"""

    def __init__(self, message: str = "Forbidden: bot was blocked or has no rights"):
        super().__init__(message, 403)


class NotFoundError(TelegramAPIError):
    """Zasób nie istnieje (404 Not Found)"""

    def __init__(self, message: str = "Not Found"):
        super().__init__(message, 404)


class BadRequestError(TelegramAPIError):
    """Nieprawidłowe parametry zapytania (400 Bad Request)"""

    def __init__(self, message: str):
        super().__init__(message, 400)


class ConflictError(TelegramAPIError):
    """Konflikt webhooka (409 Conflict)"""

    def __init__(self, message: str = "Conflict: webhook already set"):
        super().__init__(message, 409)


class UnauthorizedError(TelegramAPIError):
    """Nieautoryzowany dostęp (401 Unauthorized)"""

    def __init__(self, message: str = "Unauthorized: invalid token"):
        super().__init__(message, 401)


class TimeoutError(TelegramError):
    """Przekroczono czas oczekiwania na odpowiedź"""

    def __init__(self, message: str = "Request timeout"):
        self.message = message
        super().__init__(message)


class SkipHandler(Exception):
    """Wyjatek do pominięcia bieżącego handlera"""
    pass


class CancelHandler(Exception):
    """Wyjatek do anulowania całego przetwarzania"""
    pass


class ValidationError(TelegramError):
    """Błąd walidacji danych"""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        self.message = message
        super().__init__(f"Validation error{f' in field {field}' if field else ''}: {message}")


class WebhookError(TelegramError):
    """Błąd związany z webhookiem"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"Webhook error: {message}")


class FSMError(TelegramError):
    """Błąd związany z Finite State Machine"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"FSM error: {message}")


class MiddlewareError(TelegramError):
    """Błąd w middleware"""

    def __init__(self, message: str, middleware_name: Optional[str] = None):
        self.middleware_name = middleware_name
        self.message = message
        prefix = f"Middleware '{middleware_name}' error: " if middleware_name else "Middleware error: "
        super().__init__(f"{prefix}{message}")


def handle_telegram_error(error_data: Dict) -> TelegramAPIError:
    """
    Konwertuje odpowiedź błędu z Telegram API na odpowiedni wyjątek

    Args:
        error_data: Słownik z błędem z Telegram API

    Returns:
        Odpowiedni wyjątek TelegramAPIError
    """
    error_code = error_data.get('error_code')
    description = error_data.get('description', 'Unknown error')
    parameters = error_data.get('parameters', {})

    if error_code == 400:
        return BadRequestError(description)
    elif error_code == 401:
        return UnauthorizedError(description)
    elif error_code == 403:
        return ForbiddenError(description)
    elif error_code == 404:
        return NotFoundError(description)
    elif error_code == 409:
        return ConflictError(description)
    elif error_code == 429:
        retry_after = parameters.get('retry_after', 5)
        return RateLimitError(retry_after, description)
    else:
        return TelegramAPIError(description, error_code)