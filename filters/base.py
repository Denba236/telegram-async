# filters/base.py
"""
System filtrów dla telegram_async z obsługą operatorów logicznych
"""
from abc import ABC, abstractmethod
from typing import Any, Union, Optional, Callable, List
import re
from ..types import Message, CallbackQuery, InlineQuery, Update


class Filter(ABC):
    """
    Bazowa klasa dla filtrów z obsługą operatorów logicznych

    Przykład:
        class IsPrivate(Filter):
            async def __call__(self, message: Message) -> bool:
                return message.chat.type == "private"

        # Łączenie filtrów
        filter = Command("start") & IsPrivate()
    """

    @abstractmethod
    async def __call__(self, obj: Any) -> bool:
        """Sprawdza czy obiekt przechodzi przez filtr"""
        pass

    def __and__(self, other: 'Filter') -> 'AndFilter':
        """Operator AND (&)"""
        return AndFilter(self, other)

    def __or__(self, other: 'Filter') -> 'OrFilter':
        """Operator OR (|)"""
        return OrFilter(self, other)

    def __invert__(self) -> 'NotFilter':
        """Operator NOT (~)"""
        return NotFilter(self)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class AndFilter(Filter):
    """Filtr logiczny AND - wszystkie filtry muszą być spełnione"""

    def __init__(self, *filters: Filter):
        self.filters = filters

    async def __call__(self, obj: Any) -> bool:
        for f in self.filters:
            if not await f(obj):
                return False
        return True

    def __repr__(self) -> str:
        return f"<AND {self.filters}>"


class OrFilter(Filter):
    """Filtr logiczny OR - przynajmniej jeden filtr musi być spełniony"""

    def __init__(self, *filters: Filter):
        self.filters = filters

    async def __call__(self, obj: Any) -> bool:
        for f in self.filters:
            if await f(obj):
                return True
        return False

    def __repr__(self) -> str:
        return f"<OR {self.filters}>"


class NotFilter(Filter):
    """Filtr logiczny NOT - negacja filtru"""

    def __init__(self, filter_: Filter):
        self.filter = filter_

    async def __call__(self, obj: Any) -> bool:
        return not await self.filter(obj)

    def __repr__(self) -> str:
        return f"<NOT {self.filter}>"


# Filtry dla wiadomości

class Command(Filter):
    """Filtr komend (np. /start, /help)"""

    def __init__(
            self,
            name: Union[str, List[str]],
            prefixes: str = "/",
            ignore_case: bool = True
    ):
        """
        Args:
            name: Nazwa komendy lub lista nazw
            prefixes: Prefiksy komend (domyślnie "/")
            ignore_case: Czy ignorować wielkość liter
        """
        self.names = [name] if isinstance(name, str) else name
        self.prefixes = prefixes
        self.ignore_case = ignore_case

    async def __call__(self, message: Message) -> bool:
        if not message or not message.text:
            return False

        text = message.text
        if not text:
            return False

        # Sprawdź prefiks
        if not text[0] in self.prefixes:
            return False

        # Wyciągnij komendę
        cmd_parts = text.split()
        cmd = cmd_parts[0][1:]  # Usuń prefiks

        # Usuń @username jeśli jest
        if '@' in cmd:
            cmd = cmd.split('@')[0]

        if self.ignore_case:
            cmd = cmd.lower()
            names = [n.lower() for n in self.names]
        else:
            names = self.names

        return cmd in names


class Text(Filter):
    """Filtr dla tekstu wiadomości"""

    def __init__(
            self,
            text: Union[str, Callable[[str], bool]],
            ignore_case: bool = True,
            contains: bool = False,
            startswith: Optional[str] = None,
            endswith: Optional[str] = None,
            regex: Optional[str] = None
    ):
        """
        Args:
            text: Tekst lub funkcja sprawdzająca
            ignore_case: Czy ignorować wielkość liter
            contains: Czy tekst ma zawierać (a nie być równy)
            startswith: Czy tekst zaczyna się od
            endswith: Czy tekst kończy się na
            regex: Wyrażenie regularne
        """
        self.text = text
        self.ignore_case = ignore_case
        self.contains = contains
        self.startswith = startswith
        self.endswith = endswith
        self.regex = regex if regex is None else re.compile(regex, re.IGNORECASE if ignore_case else 0)

    async def __call__(self, message: Message) -> bool:
        if not message or not message.text:
            return False

        text = message.text

        if self.regex:
            return bool(self.regex.search(text))

        if self.startswith:
            if self.ignore_case:
                return text.lower().startswith(self.startswith.lower())
            return text.startswith(self.startswith)

        if self.endswith:
            if self.ignore_case:
                return text.lower().endswith(self.endswith.lower())
            return text.endswith(self.endswith)

        if self.contains:
            if self.ignore_case:
                text_lower = text.lower()
                search_text = self.text.lower() if isinstance(self.text, str) else self.text
                return search_text in text_lower if isinstance(search_text, str) else False

        if callable(self.text):
            return self.text(text)

        if self.ignore_case:
            return text.lower() == self.text.lower()
        return text == self.text


class IsPrivate(Filter):
    """Filtr dla czatów prywatnych"""

    async def __call__(self, message: Message) -> bool:
        return message and message.chat.type == "private"


class IsGroup(Filter):
    """Filtr dla grup"""

    async def __call__(self, message: Message) -> bool:
        return message and message.chat.type in ["group", "supergroup"]


class IsChannel(Filter):
    """Filtr dla kanałów"""

    async def __call__(self, message: Message) -> bool:
        return message and message.chat.type == "channel"


class IsReply(Filter):
    """Filtr dla wiadomości będących odpowiedziami"""

    async def __call__(self, message: Message) -> bool:
        return message and message.reply_to_message is not None


class HasMedia(Filter):
    """Filtr dla wiadomości z mediami"""

    async def __call__(self, message: Message) -> bool:
        if not message:
            return False
        return bool(
            message.photo or
            message.video or
            message.document or
            message.audio or
            message.voice or
            message.animation or
            message.sticker
        )


class HasPhoto(Filter):
    """Filtr dla wiadomości ze zdjęciami"""

    async def __call__(self, message: Message) -> bool:
        return message and bool(message.photo)


class HasDocument(Filter):
    """Filtr dla wiadomości z dokumentami"""

    async def __call__(self, message: Message) -> bool:
        return message and bool(message.document)


class FromUser(Filter):
    """Filtr dla konkretnego użytkownika"""

    def __init__(self, user_id: Union[int, List[int]]):
        self.user_ids = [user_id] if isinstance(user_id, int) else user_id

    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        user_id = None
        if isinstance(obj, Message):
            user_id = obj.from_user.id if obj.from_user else None
        elif isinstance(obj, CallbackQuery):
            user_id = obj.from_user.id

        return user_id in self.user_ids if user_id else False


class FromChat(Filter):
    """Filtr dla konkretnego czatu"""

    def __init__(self, chat_id: Union[int, List[int]]):
        self.chat_ids = [chat_id] if isinstance(chat_id, int) else chat_id

    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        chat_id = None
        if isinstance(obj, Message):
            chat_id = obj.chat.id
        elif isinstance(obj, CallbackQuery) and obj.message:
            chat_id = obj.message.chat.id

        return chat_id in self.chat_ids if chat_id else False


# Filtry dla callback query

class CallbackData(Filter):
    """Filtr dla danych callback query"""

    def __init__(
            self,
            data: Union[str, Callable[[str], bool]],
            contains: bool = False,
            regex: Optional[str] = None
    ):
        """
        Args:
            data: Oczekiwana wartość data lub funkcja
            contains: Czy data ma zawierać (a nie być równa)
            regex: Wyrażenie regularne
        """
        self.data = data
        self.contains = contains
        self.regex = regex if regex is None else re.compile(regex)

    async def __call__(self, callback: CallbackQuery) -> bool:
        if not callback or not callback.data:
            return False

        if self.regex:
            return bool(self.regex.search(callback.data))

        if self.contains:
            if isinstance(self.data, str):
                return self.data in callback.data
            return False

        if callable(self.data):
            return self.data(callback.data)

        return callback.data == self.data


class CallbackMessage(Filter):
    """Filtr dla wiadomości w callback query"""

    def __init__(self, message_filter: Filter):
        self.message_filter = message_filter

    async def __call__(self, callback: CallbackQuery) -> bool:
        if not callback or not callback.message:
            return False
        return await self.message_filter(callback.message)


# Filtry dla inline query

class InlineQuery(Filter):
    """Filtr dla zapytań inline"""

    def __init__(
            self,
            query: Optional[Union[str, Callable]] = None,
            offset: Optional[str] = None
    ):
        self.query = query
        self.offset = offset

    async def __call__(self, inline_query: InlineQuery) -> bool:
        if not inline_query:
            return False

        if self.query:
            if callable(self.query):
                if not self.query(inline_query.query):
                    return False
            elif self.query != inline_query.query:
                return False

        if self.offset and self.offset != inline_query.offset:
            return False

        return True


# Filtry dla stanów

class State(Filter):
    """Filtr dla stanów FSM"""

    def __init__(self, state: Optional[str] = None):
        """
        Args:
            state: Oczekiwany stan (None oznacza dowolny stan)
        """
        self.state = state
        self._state_filter = state  # Dla kompatybilności z dispatcher.py

    async def __call__(self, obj: Any) -> bool:
        # Ten filtr jest obsługiwany przez dispatcher
        return True


# Filtry kombinowane

class AnyFilter(Filter):
    """Filtr akceptujący jeśli którykolwiek z filtrów przejdzie (alias OR)"""

    def __init__(self, *filters: Filter):
        self.filters = filters

    async def __call__(self, obj: Any) -> bool:
        for f in self.filters:
            if await f(obj):
                return True
        return False


class AllFilter(Filter):
    """Filtr akceptujący jeśli wszystkie filtry przejdą (alias AND)"""

    def __init__(self, *filters: Filter):
        self.filters = filters

    async def __call__(self, obj: Any) -> bool:
        for f in self.filters:
            if not await f(obj):
                return False
        return True


# Funkcje pomocnicze do tworzenia filtrów

def command(name: Union[str, List[str]]) -> Command:
    """Pomocnik do tworzenia filtra Command"""
    return Command(name)


def text(
        pattern: Optional[str] = None,
        contains: bool = False,
        regex: Optional[str] = None,
        ignore_case: bool = True
) -> Text:
    """Pomocnik do tworzenia filtra Text"""
    if regex:
        return Text(regex=regex, ignore_case=ignore_case)
    if pattern:
        return Text(pattern, ignore_case=ignore_case, contains=contains)
    return Text(ignore_case=ignore_case)


def callback_data(
        data: Optional[str] = None,
        regex: Optional[str] = None,
        contains: bool = False
) -> CallbackData:
    """Pomocnik do tworzenia filtra CallbackData"""
    if regex:
        return CallbackData(regex=regex)
    if data:
        return CallbackData(data, contains=contains)
    return CallbackData(lambda x: True)


def from_user(user_id: int) -> FromUser:
    """Pomocnik do tworzenia filtra FromUser"""
    return FromUser(user_id)


def from_chat(chat_id: int) -> FromChat:
    """Pomocnik do tworzenia filtra FromChat"""
    return FromChat(chat_id)


# Predefiniowane filtry
is_private = IsPrivate()
is_group = IsGroup()
is_channel = IsChannel()
is_reply = IsReply()
has_media = HasMedia()
has_photo = HasPhoto()
has_document = HasDocument()