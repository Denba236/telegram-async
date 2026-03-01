from dataclasses import dataclass
from typing import Optional, Dict, List

from .user import User
from .message import Message
from .misc import Location


@dataclass
class InlineQuery:
    """Zapytanie inline"""
    id: str
    from_user: User
    query: str
    offset: str
    chat_type: Optional[str] = None
    location: Optional[Location] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'InlineQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            query=data['query'],
            offset=data['offset'],
            chat_type=data.get('chat_type'),
            location=Location.from_dict(data['location']) if 'location' in data else None
        )


@dataclass
class ChosenInlineResult:
    """Wybrany wynik inline"""
    result_id: str
    from_user: User
    query: str
    location: Optional[Location] = None
    inline_message_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ChosenInlineResult':
        return cls(
            result_id=data['result_id'],
            from_user=User.from_dict(data['from']),
            query=data['query'],
            location=Location.from_dict(data['location']) if 'location' in data else None,
            inline_message_id=data.get('inline_message_id')
        )


@dataclass
class CallbackQuery:
    """Zapytanie zwrotne z przycisku inline"""
    id: str
    from_user: User
    message: Optional[Message] = None
    inline_message_id: Optional[str] = None
    chat_instance: Optional[str] = None
    data: Optional[str] = None
    game_short_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'CallbackQuery':
        return cls(
            id=data['id'],
            from_user=User.from_dict(data['from']),
            message=Message.from_dict(data['message']) if 'message' in data else None,
            inline_message_id=data.get('inline_message_id'),
            chat_instance=data.get('chat_instance'),
            data=data.get('data'),
            game_short_name=data.get('game_short_name')
        )