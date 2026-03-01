from typing import Optional, Dict, Any, Union

from ..types import Message, CallbackQuery, Update
from ..client import TelegramClient


class Context:
    """Kontekst dla handlerów"""

    def __init__(self, client: TelegramClient, update: Update):
        self.client = client
        self.update = update
        self.message: Optional[Message] = update.message
        self.callback_query: Optional[CallbackQuery] = update.callback_query
        self.edited_message: Optional[Message] = update.edited_message
        self.data: Dict[str, Any] = {}  # miejsce na dane użytkownika
        self.fsm = None  # będzie ustawione przez dispatcher

    @property
    def chat_id(self) -> Optional[int]:
        if self.message:
            return self.message.chat.id
        elif self.callback_query and self.callback_query.message:
            return self.callback_query.message.chat.id
        elif self.edited_message:
            return self.edited_message.chat.id
        return None

    @property
    def user_id(self) -> Optional[int]:
        if self.message and self.message.from_user:
            return self.message.from_user.id
        elif self.callback_query:
            return self.callback_query.from_user.id
        elif self.edited_message and self.edited_message.from_user:
            return self.edited_message.from_user.id
        return None

    @property
    def text(self) -> Optional[str]:
        """Zwraca tekst wiadomości"""
        if self.message:
            return self.message.text or self.message.caption
        elif self.edited_message:
            return self.edited_message.text or self.edited_message.caption
        return None

    async def answer(self, text: str, **kwargs):
        """
        Odpowiada na wiadomość (alias dla reply)
        Dodane dla kompatybilności z kodem który używa answer()
        """
        return await self.reply(text, **kwargs)

    async def reply(self, text: str, **kwargs):
        """Odpowiada na wiadomość"""
        if self.chat_id:
            return await self.client.send_message(self.chat_id, text, **kwargs)
        return None

    async def reply_text(self, text: str, **kwargs):
        """Alias dla reply"""
        return await self.reply(text, **kwargs)

    async def answer_callback(self, text: str = None, show_alert: bool = False):
        """Odpowiada na callback query"""
        if self.callback_query:
            return await self.client.answer_callback_query(
                self.callback_query.id,
                text,
                show_alert
            )

    async def edit_message(self, text: str, reply_markup: Optional[Dict] = None):
        """Edytuje wiadomość"""
        if self.message:
            return await self.client.edit_message_text(
                text,
                chat_id=self.message.chat.id,
                message_id=self.message.message_id,
                reply_markup=reply_markup
            )
        elif self.callback_query and self.callback_query.message:
            return await self.client.edit_message_text(
                text,
                chat_id=self.callback_query.message.chat.id,
                message_id=self.callback_query.message.message_id,
                reply_markup=reply_markup
            )
        elif self.edited_message:
            return await self.client.edit_message_text(
                text,
                chat_id=self.edited_message.chat.id,
                message_id=self.edited_message.message_id,
                reply_markup=reply_markup
            )
        return None

    async def delete_message(self):
        """Usuwa wiadomość"""
        if self.message:
            return await self.client.delete_message(
                self.message.chat.id,
                self.message.message_id
            )
        return None