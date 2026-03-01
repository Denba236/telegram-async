from dataclasses import dataclass
from typing import Optional, Dict, List

from .user import User
from .message import Message
from .inline import InlineQuery, ChosenInlineResult, CallbackQuery
from .misc import Poll
from .payments import ShippingQuery, PreCheckoutQuery
from .chat_member import ChatMemberUpdated, ChatJoinRequest
from .poll_answer import PollAnswer


@dataclass
class Update:
    """Aktualizacja z Telegram API"""
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[ShippingQuery] = None
    pre_checkout_query: Optional[PreCheckoutQuery] = None
    poll: Optional[Poll] = None
    poll_answer: Optional[PollAnswer] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None
    chat_join_request: Optional[ChatJoinRequest] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Update':
        return cls(
            update_id=data['update_id'],
            message=Message.from_dict(data['message']) if 'message' in data else None,
            edited_message=Message.from_dict(data['edited_message']) if 'edited_message' in data else None,
            channel_post=Message.from_dict(data['channel_post']) if 'channel_post' in data else None,
            edited_channel_post=Message.from_dict(
                data['edited_channel_post']) if 'edited_channel_post' in data else None,
            inline_query=InlineQuery.from_dict(data['inline_query']) if 'inline_query' in data else None,
            chosen_inline_result=ChosenInlineResult.from_dict(
                data['chosen_inline_result']) if 'chosen_inline_result' in data else None,
            callback_query=CallbackQuery.from_dict(data['callback_query']) if 'callback_query' in data else None,
            shipping_query=ShippingQuery.from_dict(data['shipping_query']) if 'shipping_query' in data else None,
            pre_checkout_query=PreCheckoutQuery.from_dict(
                data['pre_checkout_query']) if 'pre_checkout_query' in data else None,
            poll=Poll.from_dict(data['poll']) if 'poll' in data else None,
            poll_answer=PollAnswer.from_dict(data['poll_answer']) if 'poll_answer' in data else None,
            my_chat_member=ChatMemberUpdated.from_dict(data['my_chat_member']) if 'my_chat_member' in data else None,
            chat_member=ChatMemberUpdated.from_dict(data['chat_member']) if 'chat_member' in data else None,
            chat_join_request=ChatJoinRequest.from_dict(
                data['chat_join_request']) if 'chat_join_request' in data else None
        )