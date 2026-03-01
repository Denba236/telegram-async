from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class User:
    """Obiekt reprezentujący użytkownika Telegram"""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    can_join_groups: Optional[bool] = None
    can_read_all_group_messages: Optional[bool] = None
    supports_inline_queries: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(
            id=data['id'],
            is_bot=data.get('is_bot', False),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name'),
            username=data.get('username'),
            language_code=data.get('language_code'),
            can_join_groups=data.get('can_join_groups'),
            can_read_all_group_messages=data.get('can_read_all_group_messages'),
            supports_inline_queries=data.get('supports_inline_queries')
        )


@dataclass
class ChatPhoto:
    """Zdjęcie czatu"""
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatPhoto':
        return cls(
            small_file_id=data['small_file_id'],
            small_file_unique_id=data['small_file_unique_id'],
            big_file_id=data['big_file_id'],
            big_file_unique_id=data['big_file_unique_id']
        )


@dataclass
class ChatPermissions:
    """Uprawnienia czatu"""
    can_send_messages: Optional[bool] = None
    can_send_media_messages: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatPermissions':
        return cls(
            can_send_messages=data.get('can_send_messages'),
            can_send_media_messages=data.get('can_send_media_messages'),
            can_send_polls=data.get('can_send_polls'),
            can_send_other_messages=data.get('can_send_other_messages'),
            can_add_web_page_previews=data.get('can_add_web_page_previews'),
            can_change_info=data.get('can_change_info'),
            can_invite_users=data.get('can_invite_users'),
            can_pin_messages=data.get('can_pin_messages')
        )


@dataclass
class Location:
    """Lokalizacja"""
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float] = None
    live_period: Optional[int] = None
    heading: Optional[int] = None
    proximity_alert_radius: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Location':
        return cls(
            longitude=data['longitude'],
            latitude=data['latitude'],
            horizontal_accuracy=data.get('horizontal_accuracy'),
            live_period=data.get('live_period'),
            heading=data.get('heading'),
            proximity_alert_radius=data.get('proximity_alert_radius')
        )


@dataclass
class ChatLocation:
    """Lokalizacja czatu"""
    location: Location
    address: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatLocation':
        return cls(
            location=Location.from_dict(data['location']),
            address=data['address']
        )


@dataclass
class Chat:
    """Obiekt reprezentujący czat"""
    id: int
    type: str  # 'private', 'group', 'supergroup', 'channel'
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None  # Odwołanie do Message jako string
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[bool] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[bool] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Chat':
        # Import wewnątrz metody, aby uniknąć cyklicznego importu
        from .message import Message

        return cls(
            id=data['id'],
            type=data['type'],
            title=data.get('title'),
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            photo=ChatPhoto.from_dict(data['photo']) if 'photo' in data else None,
            bio=data.get('bio'),
            description=data.get('description'),
            invite_link=data.get('invite_link'),
            pinned_message=Message.from_dict(data['pinned_message']) if 'pinned_message' in data else None,
            permissions=ChatPermissions.from_dict(data['permissions']) if 'permissions' in data else None,
            slow_mode_delay=data.get('slow_mode_delay'),
            message_auto_delete_time=data.get('message_auto_delete_time'),
            has_protected_content=data.get('has_protected_content'),
            sticker_set_name=data.get('sticker_set_name'),
            can_set_sticker_set=data.get('can_set_sticker_set'),
            linked_chat_id=data.get('linked_chat_id'),
            location=ChatLocation.from_dict(data['location']) if 'location' in data else None
        )