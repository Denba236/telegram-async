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

    # ==================== Payment Methods ====================

    @property
    def shipping_query(self):
        """Returns shipping query if present"""
        return self.update.shipping_query

    @property
    def pre_checkout_query(self):
        """Returns pre-checkout query if present"""
        return self.update.pre_checkout_query

    @property
    def successful_payment(self):
        """Returns successful payment info if present"""
        if self.message:
            return self.message.successful_payment
        return None

    @property
    def invoice_payload(self):
        """Returns invoice payload from pre-checkout query or message"""
        if self.pre_checkout_query:
            return self.pre_checkout_query.invoice_payload
        elif self.successful_payment:
            return self.successful_payment.invoice_payload
        return None

    async def answer_shipping_query(self, ok: bool, shipping_options: Optional[list] = None, error_message: Optional[str] = None):
        """
        Answers a shipping query
        
        Args:
            ok: True if shipping is possible
            shipping_options: List of shipping options (required if ok=True)
            error_message: Error message (required if ok=False)
        """
        if self.shipping_query:
            return await self.client.answer_shipping_query(
                self.shipping_query.id,
                ok,
                shipping_options,
                error_message
            )
        return None

    async def answer_pre_checkout_query(self, ok: bool, error_message: Optional[str] = None):
        """
        Answers a pre-checkout query
        
        Args:
            ok: True if payment can proceed
            error_message: Error message (required if ok=False)
        """
        if self.pre_checkout_query:
            return await self.client.answer_pre_checkout_query(
                self.pre_checkout_query.id,
                ok,
                error_message
            )
        return None

    async def send_invoice(self, title: str, description: str, payload: str, 
                          provider_token: str, currency: str, prices: list,
                          **kwargs):
        """
        Sends an invoice
        
        Args:
            title: Product name
            description: Product description
            payload: Bot-defined invoice payload
            provider_token: Payments provider token (empty string for XTR/Stars)
            currency: ISO 4217 currency code (e.g., 'USD', 'PLN', 'XTR')
            prices: List of price breakdowns
            **kwargs: Additional arguments (need_email, need_name, etc.)
        """
        if self.chat_id:
            # Convert LabeledPrice objects to dicts if needed
            formatted_prices = []
            for price in prices:
                if hasattr(price, 'to_dict'):
                    formatted_prices.append(price.to_dict())
                else:
                    formatted_prices.append(price)
            
            return await self.client.send_invoice(
                chat_id=self.chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token=provider_token,
                currency=currency,
                prices=formatted_prices,
                **kwargs
            )
        return None
