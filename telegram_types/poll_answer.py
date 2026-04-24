from dataclasses import dataclass
from typing import Optional, Dict, List

from .user import User


@dataclass
class PollAnswer:
    """Poll answer"""
    poll_id: str
    user: User
    option_ids: List[int]
    option_persistent_ids: Optional[List[str]] = None  # API 9.6

    @classmethod
    def from_dict(cls, data: Dict) -> 'PollAnswer':
        return cls(
            poll_id=data['poll_id'],
            user=User.from_dict(data['user']),
            option_ids=data['option_ids'],
            option_persistent_ids=data.get('option_persistent_ids')
        )
