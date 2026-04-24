
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


class MessageError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z wiadomościami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class MessageNotModifiedError(MessageError):
    """Wiadomość nie została zmodyfikowana (treść jest taka sama)"""

    def __init__(self, message: str = "Message is not modified"):
        super().__init__(message, 400)


class MessageNotFoundError(MessageError):
    """Wiadomość nie została znaleziona"""

    def __init__(self, message: str = "Message not found"):
        super().__init__(message, 404)


class MessageToDeleteError(MessageError):
    """Nie można usunąć wiadomości (np. zbyt stara)"""

    def __init__(self, message: str = "Message can't be deleted"):
        super().__init__(message, 400)


class MessageToForwardError(MessageError):
    """Nie można przekazać wiadomości"""

    def __init__(self, message: str = "Message can't be forwarded"):
        super().__init__(message, 400)


class MessageToReplyError(MessageError):
    """Nie można odpowiedzieć na wiadomość"""

    def __init__(self, message: str = "Message can't be replied"):
        super().__init__(message, 400)


class MessageCaptionTooLongError(MessageError):
    """Podpis wiadomości jest zbyt długi"""

    def __init__(self, message: str = "Message caption is too long"):
        super().__init__(message, 400)


class MessageEntitiesTooLongError(MessageError):
    """Encje wiadomości są zbyt długie"""

    def __init__(self, message: str = "Message entities are too long"):
        super().__init__(message, 400)


class ReplyMarkupError(TelegramAPIError):
    """Błąd związana z klawiaturą/reply markup"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class ReplyMarkupTooLongError(ReplyMarkupError):
    """Reply markup jest zbyt długi"""

    def __init__(self, message: str = "Reply markup is too long"):
        super().__init__(message, 400)


class ReplyMarkupInvalidError(ReplyMarkupError):
    """Nieprawidłowy reply markup"""

    def __init__(self, message: str = "Reply markup is invalid"):
        super().__init__(message, 400)


class ButtonDataInvalidError(ReplyMarkupError):
    """Nieprawidłowe dane przycisku"""

    def __init__(self, message: str = "Button data is invalid"):
        super().__init__(message, 400)


class ChatError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z czatem"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class ChatNotFoundError(ChatError):
    """Czat nie został znaleziony"""

    def __init__(self, message: str = "Chat not found"):
        super().__init__(message, 404)


class ChatRestrictedError(ChatError):
    """Dostęp do czatu jest ograniczony"""

    def __init__(self, message: str = "Chat access restricted"):
        super().__init__(message, 403)


class CantInitiateConversationError(ChatError):
    """Nie można zainicjować rozmowy"""

    def __init__(self, message: str = "Can't initiate conversation with user"):
        super().__init__(message, 403)


class CantTalkWithBotsError(ChatError):
    """Bot nie może rozmawiać z innymi botami"""

    def __init__(self, message: str = "Can't talk with other bots"):
        super().__init__(message, 400)


class UserError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z użytkownikami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class UserNotFoundError(UserError):
    """Użytkownik nie został znaleziony"""

    def __init__(self, message: str = "User not found"):
        super().__init__(message, 404)


class UserIsBotError(UserError):
    """Docelowy użytkownik jest botem"""

    def __init__(self, message: str = "Target user is a bot"):
        super().__init__(message, 400)


class AdminRequiredError(UserError):
    """Wymagane są uprawnienia administratora"""

    def __init__(self, message: str = "Admin rights required"):
        super().__init__(message, 403)


class UserIsDeactivatedError(UserError):
    """Użytkownik został dezaktywowany"""

    def __init__(self, message: str = "User is deactivated"):
        super().__init__(message, 403)


class UserIsKickedError(UserError):
    """Użytkownik został usunięty z grupy"""

    def __init__(self, message: str = "User is kicked from the group"):
        super().__init__(message, 403)


class UserIsRestrictedError(UserError):
    """Użytkownik ma nałożone ograniczenia"""

    def __init__(self, message: str = "User is restricted"):
        super().__init__(message, 403)


class UserAlreadyParticipantError(UserError):
    """Użytkownik jest już uczestnikiem czatu"""

    def __init__(self, message: str = "User is already a participant"):
        super().__init__(message, 400)


class UserNotParticipantError(UserError):
    """Użytkownik nie jest uczestnikiem czatu"""

    def __init__(self, message: str = "User is not a participant"):
        super().__init__(message, 400)


class BotAlreadyUsedError(UserError):
    """Bot był już używany/użyty"""

    def __init__(self, message: str = "Bot has already been used"):
        super().__init__(message, 400)


# ==================== Group/Supergroup Management Errors ====================

class GroupError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z grupami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class GroupMigratedError(GroupError):
    """Grupa została zaktualizowana do supergrupy"""

    def __init__(self, message: str = "Group migrated to supergroup"):
        super().__init__(message, 400)


class ChatTitleInvalidError(GroupError):
    """Nieprawidłowy tytuł czatu"""

    def __init__(self, message: str = "Invalid chat title"):
        super().__init__(message, 400)


class ChatDescriptionInvalidError(GroupError):
    """Nieprawidłowy opis czatu"""

    def __init__(self, message: str = "Invalid chat description"):
        super().__init__(message, 400)


class ChatPhotoInvalidError(GroupError):
    """Nieprawidłowe zdjęcie czatu"""

    def __init__(self, message: str = "Invalid chat photo"):
        super().__init__(message, 400)


class ChatInviteLinkInvalidError(GroupError):
    """Nieprawidłowy link zaproszenia"""

    def __init__(self, message: str = "Invalid chat invite link"):
        super().__init__(message, 400)


class ChatAdministratorsRequiredError(GroupError):
    """Wymagane uprawnienia administratora"""

    def __init__(self, message: str = "Chat administrators required"):
        super().__init__(message, 403)


class UserIsAdministratorError(GroupError):
    """Użytkownik jest już administratorem"""

    def __init__(self, message: str = "User is already an administrator"):
        super().__init__(message, 400)


# ==================== Media/File Errors ====================

class MediaError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z mediami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class FileTooLargeError(MediaError):
    """Plik przekracza limit rozmiaru"""

    def __init__(self, message: str = "File is too large"):
        super().__init__(message, 400)


class FileInvalidError(MediaError):
    """Nieprawidłowy plik"""

    def __init__(self, message: str = "File is invalid"):
        super().__init__(message, 400)


class FileTypeNotSupportedError(MediaError):
    """Typ pliku nie jest obsługiwany"""

    def __init__(self, message: str = "File type is not supported"):
        super().__init__(message, 400)


class PhotoDimensionsInvalidError(MediaError):
    """Nieprawidłowe wymiary zdjęcia"""

    def __init__(self, message: str = "Invalid photo dimensions"):
        super().__init__(message, 400)


class VideoDurationTooLongError(MediaError):
    """Czas trwania wideo jest zbyt długi"""

    def __init__(self, message: str = "Video duration is too long"):
        super().__init__(message, 400)


class AudioDurationInvalidError(MediaError):
    """Nieprawidłowy czas trwania audio"""

    def __init__(self, message: str = "Invalid audio duration"):
        super().__init__(message, 400)


class DocumentMimeTypeInvalidError(MediaError):
    """Nieprawidłowy typ MIME dokumentu"""

    def __init__(self, message: str = "Invalid document MIME type"):
        super().__init__(message, 400)


# ==================== Sticker/Animation Errors ====================

class StickerError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych ze stickerami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class StickerSetInvalidError(StickerError):
    """Nieprawidłowy zestaw stickerów"""

    def __init__(self, message: str = "Invalid sticker set"):
        super().__init__(message, 400)


class StickerEmojiInvalidError(StickerError):
    """Nieprawidłowy emoji stickera"""

    def __init__(self, message: str = "Invalid sticker emoji"):
        super().__init__(message, 400)


class StickerPngDimensionsInvalidError(StickerError):
    """Nieprawidłowe wymiary PNG stickera"""

    def __init__(self, message: str = "Invalid sticker PNG dimensions"):
        super().__init__(message, 400)


class StickerTgsInvalidError(StickerError):
    """Nieprawidłowy sticker animowany (TGS)"""

    def __init__(self, message: str = "Invalid TGS animated sticker"):
        super().__init__(message, 400)


class AnimationInvalidError(StickerError):
    """Nieprawidłowa animacja/GIF"""

    def __init__(self, message: str = "Invalid animation/GIF"):
        super().__init__(message, 400)


# ==================== Location/Venue Errors ====================

class LocationError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z lokalizacją"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class LocationInvalidError(LocationError):
    """Nieprawidłowe dane lokalizacji"""

    def __init__(self, message: str = "Invalid location data"):
        super().__init__(message, 400)


class VenueInvalidError(LocationError):
    """Nieprawidłowe dane miejsca"""

    def __init__(self, message: str = "Invalid venue data"):
        super().__init__(message, 400)


class LiveLocationPeriodExpiredError(LocationError):
    """Okres lokalizacji na żywo wygasł"""

    def __init__(self, message: str = "Live location period expired"):
        super().__init__(message, 400)


class LiveLocationAlreadyStoppedError(LocationError):
    """Lokalizacja na żywo już zatrzymana"""

    def __init__(self, message: str = "Live location already stopped"):
        super().__init__(message, 400)


# ==================== Contact/Poll Errors ====================

class ContactError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z kontaktami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class ContactUserIdInvalidError(ContactError):
    """Nieprawidłowe ID użytkownika kontaktu"""

    def __init__(self, message: str = "Invalid contact user ID"):
        super().__init__(message, 400)


class ContactPhoneNumberInvalidError(ContactError):
    """Nieprawidłowy numer telefonu kontaktu"""

    def __init__(self, message: str = "Invalid contact phone number"):
        super().__init__(message, 400)


class PollError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z ankietami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class PollAlreadyClosedError(PollError):
    """Ankieta jest już zamknięta"""

    def __init__(self, message: str = "Poll is already closed"):
        super().__init__(message, 400)


class PollAlreadyExistsError(PollError):
    """Ankieta już istnieje w wiadomości"""

    def __init__(self, message: str = "Poll already exists in message"):
        super().__init__(message, 400)


class PollQuestionInvalidError(PollError):
    """Nieprawidłowe pytanie ankiety"""

    def __init__(self, message: str = "Invalid poll question"):
        super().__init__(message, 400)


class PollOptionsInvalidError(PollError):
    """Nieprawidłowe opcje ankiety (za mało/za dużo)"""

    def __init__(self, message: str = "Invalid poll options"):
        super().__init__(message, 400)


class PollOptionsTypeInvalidError(PollError):
    """Nieprawidłowy typ opcji ankiety"""

    def __init__(self, message: str = "Invalid poll options type"):
        super().__init__(message, 400)


# ==================== Inline Query Errors ====================

class InlineQueryError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z inline query"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class InlineQueryIdInvalidError(InlineQueryError):
    """Nieprawidłowe ID inline query"""

    def __init__(self, message: str = "Invalid inline query ID"):
        super().__init__(message, 400)


class InlineQueryResultInvalidError(InlineQueryError):
    """Nieprawidłowy wynik inline query"""

    def __init__(self, message: str = "Invalid inline query result"):
        super().__init__(message, 400)


class InlineQueryResultsTooManyError(InlineQueryError):
    """Za dużo wyników inline query"""

    def __init__(self, message: str = "Too many inline query results"):
        super().__init__(message, 400)


class SwitchPmTextInvalidError(InlineQueryError):
    """Nieprawidłowy tekst switch PM"""

    def __init__(self, message: str = "Invalid switch PM text"):
        super().__init__(message, 400)


class SwitchPmParameterInvalidError(InlineQueryError):
    """Nieprawidłowy parametr switch PM"""

    def __init__(self, message: str = "Invalid switch PM parameter"):
        super().__init__(message, 400)


# ==================== Callback Query Errors ====================

class CallbackQueryError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z callback query"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class CallbackQueryIdInvalidError(CallbackQueryError):
    """Nieprawidłowe ID callback query"""

    def __init__(self, message: str = "Invalid callback query ID"):
        super().__init__(message, 400)


class CallbackQueryDataTooLongError(CallbackQueryError):
    """Dane callback query są zbyt długie"""

    def __init__(self, message: str = "Callback query data is too long"):
        super().__init__(message, 400)


class CallbackQueryAnswerExpiredError(CallbackQueryError):
    """Odpowiedź callback query wygasła"""

    def __init__(self, message: str = "Callback query answer expired"):
        super().__init__(message, 400)


# ==================== Shipping/Order Errors ====================

class ShippingError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z wysyłką"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class ShippingAddressInvalidError(ShippingError):
    """Nieprawidłowy adres wysyłki"""

    def __init__(self, message: str = "Invalid shipping address"):
        super().__init__(message, 400)


class ShippingQueryIdInvalidError(ShippingError):
    """Nieprawidłowe ID shipping query"""

    def __init__(self, message: str = "Invalid shipping query ID"):
        super().__init__(message, 400)


class ShippingOptionInvalidError(ShippingError):
    """Nieprawidłowa opcja wysyłki"""

    def __init__(self, message: str = "Invalid shipping option"):
        super().__init__(message, 400)


class ShippingOptionsRequiredError(ShippingError):
    """Wymagane opcje wysyłki"""

    def __init__(self, message: str = "Shipping options are required"):
        super().__init__(message, 400)


class PreCheckoutQueryIdInvalidError(ShippingError):
    """Nieprawidłowe ID pre-checkout query"""

    def __init__(self, message: str = "Invalid pre-checkout query ID"):
        super().__init__(message, 400)


class OrderInfoInvalidError(ShippingError):
    """Nieprawidłowe informacje o zamówieniu"""

    def __init__(self, message: str = "Invalid order information"):
        super().__init__(message, 400)


class PaymentError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z płatnościami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class PaymentRequiredError(PaymentError):
    """Wymagana płatność"""

    def __init__(self, message: str = "Payment required"):
        super().__init__(message, 402)


class PaymentFailedError(PaymentError):
    """Płatność nie powiodła się"""

    def __init__(self, message: str = "Payment failed"):
        super().__init__(message, 400)


class InvalidInvoiceError(PaymentError):
    """Nieprawidłowy faktura/rachunek"""

    def __init__(self, message: str = "Invalid invoice"):
        super().__init__(message, 400)


class InvoiceExpiredError(PaymentError):
    """Faktura wygasła"""

    def __init__(self, message: str = "Invoice expired"):
        super().__init__(message, 400)


class CantSendInvoiceError(PaymentError):
    """Nie można wysłać faktury"""

    def __init__(self, message: str = "Can't send invoice"):
        super().__init__(message, 400)


class PaymentProviderUnavailableError(PaymentError):
    """Dostawca płatności jest niedostępny"""

    def __init__(self, message: str = "Payment provider unavailable"):
        super().__init__(message, 503)


class PaymentCurrencyNotSupportedError(PaymentError):
    """Waluta nie jest obsługiwana"""

    def __init__(self, message: str = "Currency not supported"):
        super().__init__(message, 400)


class PaymentAmountInvalidError(PaymentError):
    """Kwota płatności jest nieprawidłowa"""

    def __init__(self, message: str = "Payment amount is invalid"):
        super().__init__(message, 400)


# ==================== Broadcast/Channel Errors ====================

class ChannelError(TelegramAPIError):
    """Bazowa klasa dla błędów związanych z kanałami"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class ChannelPrivateError(ChannelError):
    """Kanał jest prywatny"""

    def __init__(self, message: str = "Channel is private"):
        super().__init__(message, 403)


class ChannelNotCreatedError(ChannelError):
    """Kanał nie istnieje"""

    def __init__(self, message: str = "Channel does not exist"):
        super().__init__(message, 404)


class BroadcastRequiredError(ChannelError):
    """Musi być kanałem broadcast"""

    def __init__(self, message: str = "Must be a broadcast channel"):
        super().__init__(message, 400)


class ChannelTooManyError(ChannelError):
    """Za dużo kanałów utworzonych"""

    def __init__(self, message: str = "Too many channels created"):
        super().__init__(message, 400)


# ==================== Rate Limiting Extended ====================

class FloodControlError(TelegramAPIError):
    """Ogólny błąd kontroli flood"""

    def __init__(self, message: str = "Flood control exceeded"):
        super().__init__(message, 420)


class SlowModeEnabledError(TelegramAPIError):
    """Tryb powolny jest włączony"""

    def __init__(self, message: str = "Slow mode is enabled"):
        super().__init__(message, 400)


class SlowModeDelayActiveError(TelegramAPIError):
    """Opóźnienie trybu powolnego jest aktywne"""

    def __init__(self, message: str = "Slow mode delay is active"):
        super().__init__(message, 400)


# ==================== Permissions Errors ====================

class PermissionError(TelegramAPIError):
    """Bazowa klasa dla błędów uprawnień"""

    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        super().__init__(message, code)


class SendMessageNotAllowedError(PermissionError):
    """Nie można wysyłać wiadomości na tym czacie"""

    def __init__(self, message: str = "Can't send messages in this chat"):
        super().__init__(message, 403)


class SendMediaNotAllowedError(PermissionError):
    """Nie można wysyłać mediów na tym czacie"""

    def __init__(self, message: str = "Can't send media in this chat"):
        super().__init__(message, 403)


class SendPollNotAllowedError(PermissionError):
    """Nie można wysyłać ankiet na tym czacie"""

    def __init__(self, message: str = "Can't send polls in this chat"):
        super().__init__(message, 403)


class SendOtherNotAllowedError(PermissionError):
    """Nie można wysyłać innych wiadomości na tym czacie"""

    def __init__(self, message: str = "Can't send other messages in this chat"):
        super().__init__(message, 403)


class ChangeInfoNotAllowedError(PermissionError):
    """Nie można zmieniać informacji o czacie"""

    def __init__(self, message: str = "Can't change chat info"):
        super().__init__(message, 403)


class InviteUserNotAllowedError(PermissionError):
    """Nie można zapraszać użytkowników na czat"""

    def __init__(self, message: str = "Can't invite users to chat"):
        super().__init__(message, 403)


class PinMessageNotAllowedError(PermissionError):
    """Nie można przypinać wiadomości"""

    def __init__(self, message: str = "Can't pin messages"):
        super().__init__(message, 403)


# ==================== Miscellaneous Errors ====================

class MethodNotAvailableInChannelError(TelegramAPIError):
    """Metoda nie jest dostępna na kanałach"""

    def __init__(self, message: str = "Method not available in channels"):
        super().__init__(message, 400)


class MethodNotAvailableInGroupError(TelegramAPIError):
    """Metoda nie jest dostępna w grupach"""

    def __init__(self, message: str = "Method not available in groups"):
        super().__init__(message, 400)


class PeerFloodError(TelegramAPIError):
    """Za dużo zapytań do tego samego peera"""

    def __init__(self, message: str = "Too many requests to same peer"):
        super().__init__(message, 420)


class PhoneNumberInvalidError(TelegramAPIError):
    """Nieprawidłowy format numeru telefonu"""

    def __init__(self, message: str = "Invalid phone number format"):
        super().__init__(message, 400)


class PhoneCodeInvalidError(TelegramAPIError):
    """Nieprawidłowy kod weryfikacyjny telefonu"""

    def __init__(self, message: str = "Invalid phone verification code"):
        super().__init__(message, 400)


class SessionExpiredError(TelegramAPIError):
    """Sesja wygasła"""

    def __init__(self, message: str = "Session has expired"):
        super().__init__(message, 401)


class AccessTokenExpiredError(TelegramAPIError):
    """Token dostępu wygasł"""

    def __init__(self, message: str = "Access token has expired"):
        super().__init__(message, 401)


class DatabaseError(TelegramAPIError):
    """Wewnętrzny błąd bazy danych"""

    def __init__(self, message: str = "Internal database error"):
        super().__init__(message, 500)


class ServerMaintenanceError(TelegramAPIError):
    """Serwer w trakcie konserwacji"""

    def __init__(self, message: str = "Server under maintenance"):
        super().__init__(message, 503)


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

    desc_lower = description.lower()

    if error_code == 400:
        # Check for specific message-related errors
        if 'not modified' in desc_lower:
            return MessageNotModifiedError(description)
        elif 'message' in desc_lower and ('delete' in desc_lower or 'can\'t be deleted' in desc_lower):
            return MessageToDeleteError(description)
        elif 'message' in desc_lower and ('forward' in desc_lower or 'can\'t be forwarded' in desc_lower):
            return MessageToForwardError(description)
        elif 'message' in desc_lower and ('reply' in desc_lower or 'can\'t be replied' in desc_lower):
            return MessageToReplyError(description)
        elif 'caption' in desc_lower and 'too long' in desc_lower:
            return MessageCaptionTooLongError(description)
        elif 'entities' in desc_lower and 'too long' in desc_lower:
            return MessageEntitiesTooLongError(description)
        elif 'reply markup' in desc_lower and 'too long' in desc_lower:
            return ReplyMarkupTooLongError(description)
        elif 'reply markup' in desc_lower and 'invalid' in desc_lower:
            return ReplyMarkupInvalidError(description)
        elif 'button' in desc_lower and 'invalid' in desc_lower:
            return ButtonDataInvalidError(description)
        elif 'bot' in desc_lower and 'talk' in desc_lower:
            return CantTalkWithBotsError(description)
        # Check for user-related errors
        elif 'user' in desc_lower and 'bot' in desc_lower:
            return UserIsBotError(description)
        elif 'user' in desc_lower and ('already' in desc_lower or 'participant' in desc_lower):
            return UserAlreadyParticipantError(description)
        elif 'user' in desc_lower and 'not' in desc_lower and 'participant' in desc_lower:
            return UserNotParticipantError(description)
        elif 'bot' in desc_lower and ('already' in desc_lower or 'used' in desc_lower):
            return BotAlreadyUsedError(description)
        # Check for group/chat errors
        elif 'migrat' in desc_lower and ('group' in desc_lower or 'supergroup' in desc_lower):
            return GroupMigratedError(description)
        elif 'chat' in desc_lower and 'title' in desc_lower and 'invalid' in desc_lower:
            return ChatTitleInvalidError(description)
        elif 'chat' in desc_lower and 'description' in desc_lower and 'invalid' in desc_lower:
            return ChatDescriptionInvalidError(description)
        elif 'chat' in desc_lower and 'photo' in desc_lower and 'invalid' in desc_lower:
            return ChatPhotoInvalidError(description)
        elif 'invite' in desc_lower and 'link' in desc_lower and 'invalid' in desc_lower:
            return ChatInviteLinkInvalidError(description)
        elif 'admin' in desc_lower and 'already' in desc_lower:
            return UserIsAdministratorError(description)
        # Check for media/file errors
        elif 'file' in desc_lower and ('too large' in desc_lower or 'size' in desc_lower):
            return FileTooLargeError(description)
        elif 'file' in desc_lower and 'invalid' in desc_lower:
            return FileInvalidError(description)
        elif 'file type' in desc_lower and 'not supported' in desc_lower:
            return FileTypeNotSupportedError(description)
        elif 'photo' in desc_lower and 'dimension' in desc_lower and 'invalid' in desc_lower:
            return PhotoDimensionsInvalidError(description)
        elif 'video' in desc_lower and ('too long' in desc_lower or 'duration' in desc_lower):
            return VideoDurationTooLongError(description)
        elif 'audio' in desc_lower and 'duration' in desc_lower and 'invalid' in desc_lower:
            return AudioDurationInvalidError(description)
        elif 'mime' in desc_lower and 'invalid' in desc_lower:
            return DocumentMimeTypeInvalidError(description)
        # Check for sticker errors
        elif 'sticker' in desc_lower and 'set' in desc_lower and 'invalid' in desc_lower:
            return StickerSetInvalidError(description)
        elif 'sticker' in desc_lower and 'emoji' in desc_lower and 'invalid' in desc_lower:
            return StickerEmojiInvalidError(description)
        elif 'sticker' in desc_lower and 'png' in desc_lower and 'dimension' in desc_lower:
            return StickerPngDimensionsInvalidError(description)
        elif 'tgs' in desc_lower or 'animated' in desc_lower:
            return StickerTgsInvalidError(description)
        elif 'animation' in desc_lower or 'gif' in desc_lower:
            return AnimationInvalidError(description)
        # Check for location errors
        elif 'location' in desc_lower and 'invalid' in desc_lower:
            return LocationInvalidError(description)
        elif 'venue' in desc_lower and 'invalid' in desc_lower:
            return VenueInvalidError(description)
        elif 'live location' in desc_lower and 'expir' in desc_lower:
            return LiveLocationPeriodExpiredError(description)
        elif 'live location' in desc_lower and 'already' in desc_lower and 'stopped' in desc_lower:
            return LiveLocationAlreadyStoppedError(description)
        # Check for contact errors
        elif 'contact' in desc_lower and 'user' in desc_lower and 'id' in desc_lower:
            return ContactUserIdInvalidError(description)
        elif 'contact' in desc_lower and 'phone' in desc_lower:
            return ContactPhoneNumberInvalidError(description)
        # Check for poll errors
        elif 'poll' in desc_lower and 'already' in desc_lower and 'closed' in desc_lower:
            return PollAlreadyClosedError(description)
        elif 'poll' in desc_lower and 'already' in desc_lower and 'exist' in desc_lower:
            return PollAlreadyExistsError(description)
        elif 'poll' in desc_lower and 'question' in desc_lower and 'invalid' in desc_lower:
            return PollQuestionInvalidError(description)
        elif 'poll' in desc_lower and 'option' in desc_lower and 'invalid' in desc_lower:
            return PollOptionsInvalidError(description)
        elif 'poll' in desc_lower and 'option' in desc_lower and 'type' in desc_lower:
            return PollOptionsTypeInvalidError(description)
        # Check for inline query errors
        elif 'inline' in desc_lower and 'query' in desc_lower and 'id' in desc_lower and 'invalid' in desc_lower:
            return InlineQueryIdInvalidError(description)
        elif 'inline' in desc_lower and 'result' in desc_lower and 'invalid' in desc_lower:
            return InlineQueryResultInvalidError(description)
        elif 'inline' in desc_lower and ('too many' in desc_lower or 'results' in desc_lower):
            return InlineQueryResultsTooManyError(description)
        elif 'switch' in desc_lower and 'pm' in desc_lower and 'text' in desc_lower:
            return SwitchPmTextInvalidError(description)
        elif 'switch' in desc_lower and 'pm' in desc_lower and 'parameter' in desc_lower:
            return SwitchPmParameterInvalidError(description)
        # Check for callback query errors
        elif 'callback' in desc_lower and 'query' in desc_lower and 'id' in desc_lower and 'invalid' in desc_lower:
            return CallbackQueryIdInvalidError(description)
        elif 'callback' in desc_lower and 'data' in desc_lower and 'too long' in desc_lower:
            return CallbackQueryDataTooLongError(description)
        elif 'callback' in desc_lower and 'answer' in desc_lower and 'expir' in desc_lower:
            return CallbackQueryAnswerExpiredError(description)
        # Check for shipping errors
        elif 'shipping' in desc_lower and 'address' in desc_lower and 'invalid' in desc_lower:
            return ShippingAddressInvalidError(description)
        elif 'shipping' in desc_lower and 'query' in desc_lower and 'id' in desc_lower:
            return ShippingQueryIdInvalidError(description)
        elif 'shipping' in desc_lower and 'option' in desc_lower and 'invalid' in desc_lower:
            return ShippingOptionInvalidError(description)
        elif 'shipping' in desc_lower and 'required' in desc_lower:
            return ShippingOptionsRequiredError(description)
        elif 'pre-checkout' in desc_lower or 'pre checkout' in desc_lower:
            return PreCheckoutQueryIdInvalidError(description)
        elif 'order' in desc_lower and 'info' in desc_lower and 'invalid' in desc_lower:
            return OrderInfoInvalidError(description)
        # Check for channel errors
        elif 'channel' in desc_lower and 'private' in desc_lower:
            return ChannelPrivateError(description)
        elif 'channel' in desc_lower and 'not' in desc_lower and 'exist' in desc_lower:
            return ChannelNotCreatedError(description)
        elif 'broadcast' in desc_lower and 'required' in desc_lower:
            return BroadcastRequiredError(description)
        elif 'too many' in desc_lower and 'channel' in desc_lower:
            return ChannelTooManyError(description)
        # Check for slow mode errors
        elif 'slow' in desc_lower and 'mode' in desc_lower and 'enabled' in desc_lower:
            return SlowModeEnabledError(description)
        elif 'slow' in desc_lower and 'mode' in desc_lower and 'delay' in desc_lower:
            return SlowModeDelayActiveError(description)
        # Check for permission errors
        elif 'send' in desc_lower and 'message' in desc_lower and 'not' in desc_lower:
            return SendMessageNotAllowedError(description)
        elif 'send' in desc_lower and 'media' in desc_lower and 'not' in desc_lower:
            return SendMediaNotAllowedError(description)
        elif 'send' in desc_lower and 'poll' in desc_lower and 'not' in desc_lower:
            return SendPollNotAllowedError(description)
        elif 'change' in desc_lower and 'info' in desc_lower and 'not' in desc_lower:
            return ChangeInfoNotAllowedError(description)
        elif 'invite' in desc_lower and 'user' in desc_lower and 'not' in desc_lower:
            return InviteUserNotAllowedError(description)
        elif 'pin' in desc_lower and 'message' in desc_lower and 'not' in desc_lower:
            return PinMessageNotAllowedError(description)
        # Check for method availability errors
        elif 'method' in desc_lower and 'not' in desc_lower and 'available' in desc_lower and 'channel' in desc_lower:
            return MethodNotAvailableInChannelError(description)
        elif 'method' in desc_lower and 'not' in desc_lower and 'available' in desc_lower and 'group' in desc_lower:
            return MethodNotAvailableInGroupError(description)
        # Check for phone errors
        elif 'phone' in desc_lower and 'number' in desc_lower and 'invalid' in desc_lower:
            return PhoneNumberInvalidError(description)
        elif 'phone' in desc_lower and 'code' in desc_lower and 'invalid' in desc_lower:
            return PhoneCodeInvalidError(description)
        # Check for payment-related errors
        elif 'invoice' in desc_lower and 'invalid' in desc_lower:
            return InvalidInvoiceError(description)
        elif 'invoice' in desc_lower and 'expired' in desc_lower:
            return InvoiceExpiredError(description)
        elif 'can\'t send invoice' in desc_lower:
            return CantSendInvoiceError(description)
        elif 'payment' in desc_lower and 'failed' in desc_lower:
            return PaymentFailedError(description)
        elif 'currency' in desc_lower and ('not supported' in desc_lower or 'unsupported' in desc_lower):
            return PaymentCurrencyNotSupportedError(description)
        elif 'amount' in desc_lower and ('invalid' in desc_lower or 'incorrect' in desc_lower):
            return PaymentAmountInvalidError(description)
        else:
            return BadRequestError(description)
    elif error_code == 401:
        if 'session' in desc_lower and 'expir' in desc_lower:
            return SessionExpiredError(description)
        elif 'access' in desc_lower and 'token' in desc_lower and 'expir' in desc_lower:
            return AccessTokenExpiredError(description)
        else:
            return UnauthorizedError(description)
    elif error_code == 402:
        return PaymentRequiredError(description)
    elif error_code == 403:
        # Check for specific chat-related errors
        if 'initiate' in desc_lower and 'conversation' in desc_lower:
            return CantInitiateConversationError(description)
        elif 'chat' in desc_lower and ('restrict' in desc_lower or 'forbidden' in desc_lower):
            return ChatRestrictedError(description)
        # Check for user-related errors
        elif 'admin' in desc_lower and ('required' in desc_lower or 'rights' in desc_lower):
            return AdminRequiredError(description)
        elif 'user' in desc_lower and ('deactivat' in desc_lower or 'banned' in desc_lower):
            return UserIsDeactivatedError(description)
        elif 'user' in desc_lower and 'kicked' in desc_lower:
            return UserIsKickedError(description)
        elif 'user' in desc_lower and 'restrict' in desc_lower:
            return UserIsRestrictedError(description)
        # Check for permission errors
        elif 'send' in desc_lower and 'message' in desc_lower and 'not' in desc_lower:
            return SendMessageNotAllowedError(description)
        elif 'send' in desc_lower and 'media' in desc_lower and 'not' in desc_lower:
            return SendMediaNotAllowedError(description)
        elif 'send' in desc_lower and 'poll' in desc_lower and 'not' in desc_lower:
            return SendPollNotAllowedError(description)
        elif 'change' in desc_lower and 'info' in desc_lower and 'not' in desc_lower:
            return ChangeInfoNotAllowedError(description)
        elif 'invite' in desc_lower and 'user' in desc_lower and 'not' in desc_lower:
            return InviteUserNotAllowedError(description)
        elif 'pin' in desc_lower and 'message' in desc_lower and 'not' in desc_lower:
            return PinMessageNotAllowedError(description)
        # Check for channel errors
        elif 'channel' in desc_lower and 'private' in desc_lower:
            return ChannelPrivateError(description)
        # Check for admin errors
        elif 'admin' in desc_lower and 'required' in desc_lower:
            return ChatAdministratorsRequiredError(description)
        else:
            return ForbiddenError(description)
    elif error_code == 404:
        # Check for specific not found errors
        if 'message' in desc_lower and 'not found' in desc_lower:
            return MessageNotFoundError(description)
        elif 'chat' in desc_lower and 'not found' in desc_lower:
            return ChatNotFoundError(description)
        elif 'user' in desc_lower and 'not found' in desc_lower:
            return UserNotFoundError(description)
        elif 'channel' in desc_lower and 'not' in desc_lower and 'exist' in desc_lower:
            return ChannelNotCreatedError(description)
        else:
            return NotFoundError(description)
    elif error_code == 409:
        return ConflictError(description)
    elif error_code == 420:
        if 'flood' in desc_lower or 'peer' in desc_lower:
            return PeerFloodError(description)
        else:
            return FloodControlError(description)
    elif error_code == 429:
        retry_after = parameters.get('retry_after', 5)
        return RateLimitError(retry_after, description)
    elif error_code == 500:
        return DatabaseError(description)
    elif error_code == 503:
        if 'maintenance' in desc_lower:
            return ServerMaintenanceError(description)
        else:
            return PaymentProviderUnavailableError(description)
    else:
        return TelegramAPIError(description, error_code)