from typing import Optional, Dict, Any, Union

from ..telegram_types import Message, CallbackQuery, Update
from ..client import TelegramClient

class Context:
    """Context object for handlers"""

    def __init__(self, client: TelegramClient, update: Update):
        self.client = client
        self.update = update
        self.message: Optional[Message] = update.message
        self.callback_query: Optional[CallbackQuery] = update.callback_query
        self.edited_message: Optional[Message] = update.edited_message
        self.data: Dict[str, Any] = {}  # space for custom user data
        self.fsm = None  # will be injected by the dispatcher

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
        """Returns the text or caption of the message/edited message"""
        if self.message:
            return self.message.text or self.message.caption
        elif self.edited_message:
            return self.edited_message.text or self.edited_message.caption
        return None

    async def answer(self, text: str, **kwargs):
        """Answers the message (alias for reply)"""
        return await self.reply(text, **kwargs)

    async def reply(self, text: str, **kwargs):
        """Replies to the message"""
        if self.chat_id:
            return await self.client.send_message(self.chat_id, text, **kwargs)
        return None

    async def reply_text(self, text: str, **kwargs):
        """Alias for reply"""
        return await self.reply(text, **kwargs)

    async def answer_callback(self, text: Optional[str] = None, show_alert: bool = False):
        """Answers a callback query"""
        if self.callback_query:
            return await self.client.answer_callback_query(
                self.callback_query.id,
                text,
                show_alert
            )

    async def edit_message(self, text: str, reply_markup: Optional[Dict] = None):
        """Edits the text of a message"""
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
        """Deletes the current message"""
        if self.message:
            return await self.client.delete_message(
                self.message.chat.id,
                self.message.message_id
            )
        return None
