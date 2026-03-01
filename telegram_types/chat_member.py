from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

from .user import User, Chat


@dataclass
class ChatMember:
    """Członek czatu"""
    status: str  # 'creator', 'administrator', 'member', 'restricted', 'left', 'kicked'
    user: User
    is_anonymous: Optional[bool] = None
    custom_title: Optional[str] = None
    can_be_edited: Optional[bool] = None
    can_manage_chat: Optional[bool] = None
    can_post_messages: Optional[bool] = None
    can_edit_messages: Optional[bool] = None
    can_delete_messages: Optional[bool] = None
    can_manage_video_chats: Optional[bool] = None
    can_restrict_members: Optional[bool] = None
    can_promote_members: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    is_member: Optional[bool] = None
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    until_date: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatMember':
        return cls(
            status=data['status'],
            user=User.from_dict(data['user']),
            is_anonymous=data.get('is_anonymous'),
            custom_title=data.get('custom_title'),
            can_be_edited=data.get('can_be_edited'),
            can_manage_chat=data.get('can_manage_chat'),
            can_post_messages=data.get('can_post_messages'),
            can_edit_messages=data.get('can_edit_messages'),
            can_delete_messages=data.get('can_delete_messages'),
            can_manage_video_chats=data.get('can_manage_video_chats'),
            can_restrict_members=data.get('can_restrict_members'),
            can_promote_members=data.get('can_promote_members'),
            can_change_info=data.get('can_change_info'),
            can_invite_users=data.get('can_invite_users'),
            can_pin_messages=data.get('can_pin_messages'),
            is_member=data.get('is_member'),
            can_send_messages=data.get('can_send_messages'),
            can_send_media_messages=data.get('can_send_media_messages'),
            can_send_polls=data.get('can_send_polls'),
            can_send_other_messages=data.get('can_send_other_messages'),
            can_add_web_page_previews=data.get('can_add_web_page_previews'),
            until_date=datetime.fromtimestamp(data['until_date']) if data.get('until_date') else None
        )


@dataclass
class ChatInviteLink:
    """Link zaproszenia do czatu"""
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[datetime] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatInviteLink':
        return cls(
            invite_link=data['invite_link'],
            creator=User.from_dict(data['creator']),
            creates_join_request=data['creates_join_request'],
            is_primary=data['is_primary'],
            is_revoked=data['is_revoked'],
            name=data.get('name'),
            expire_date=datetime.fromtimestamp(data['expire_date']) if data.get('expire_date') else None,
            member_limit=data.get('member_limit'),
            pending_join_request_count=data.get('pending_join_request_count')
        )


@dataclass
class ChatMemberUpdated:
    """Aktualizacja członka czatu"""
    chat: Chat
    from_user: User
    date: datetime
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatMemberUpdated':
        return cls(
            chat=Chat.from_dict(data['chat']),
            from_user=User.from_dict(data['from']),
            date=datetime.fromtimestamp(data['date']),
            old_chat_member=ChatMember.from_dict(data['old_chat_member']),
            new_chat_member=ChatMember.from_dict(data['new_chat_member']),
            invite_link=ChatInviteLink.from_dict(data['invite_link']) if 'invite_link' in data else None
        )


@dataclass
class ChatJoinRequest:
    """Prośba o dołączenie do czatu"""
    chat: Chat
    from_user: User
    date: datetime
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatJoinRequest':
        return cls(
            chat=Chat.from_dict(data['chat']),
            from_user=User.from_dict(data['from']),
            date=datetime.fromtimestamp(data['date']),
            bio=data.get('bio'),
            invite_link=ChatInviteLink.from_dict(data['invite_link']) if 'invite_link' in data else None
        )