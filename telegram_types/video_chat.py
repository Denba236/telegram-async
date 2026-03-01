from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

from .user import User


@dataclass
class VideoChatScheduled:
    """Zaplanowany czat wideo"""
    start_date: datetime

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatScheduled':
        return cls(
            start_date=datetime.fromtimestamp(data['start_date'])
        )


@dataclass
class VideoChatStarted:
    """Rozpoczęty czat wideo"""
    pass

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatStarted':
        return cls()


@dataclass
class VideoChatEnded:
    """Zakończony czat wideo"""
    duration: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatEnded':
        return cls(
            duration=data['duration']
        )


@dataclass
class VideoChatParticipantsInvited:
    """Zaproszeni uczestnicy czatu wideo"""
    users: List[User]

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatParticipantsInvited':
        return cls(
            users=[User.from_dict(u) for u in data['users']]
        )