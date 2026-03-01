from dataclasses import dataclass
from typing import Optional, Dict, List

from .user import User


@dataclass
class PollAnswer:
    """Odpowiedź na ankietę"""
    poll_id: str
    user: User
    option_ids: List[int]

    @classmethod
    def from_dict(cls, data: Dict) -> 'PollAnswer':
        return cls(
            poll_id=data['poll_id'],
            user=User.from_dict(data['user']),
            option_ids=data['option_ids']
        )