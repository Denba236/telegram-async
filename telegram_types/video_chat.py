from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

from .user import User


@dataclass
class VideoChatScheduled:
    """Scheduled video chat"""
    start_date: datetime

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatScheduled':
        return cls(
            start_date=datetime.fromtimestamp(data['start_date'])
        )


@dataclass
class VideoChatStarted:
    """Started video chat"""
    pass

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatStarted':
        return cls()


@dataclass
class VideoChatEnded:
    """Ended video chat"""
    duration: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatEnded':
        return cls(
            duration=data['duration']
        )


@dataclass
class VideoChatParticipantsInvited:
    """Video chat participants invited"""
    users: List[User]

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoChatParticipantsInvited':
        return cls(
            users=[User.from_dict(u) for u in data['users']]
        )
