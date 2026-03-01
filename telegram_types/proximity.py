from dataclasses import dataclass
from typing import Optional, Dict

from .user import User


@dataclass
class ProximityAlertTriggered:
    """Alert zbliżeniowy"""
    traveler: User
    watcher: User
    distance: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'ProximityAlertTriggered':
        return cls(
            traveler=User.from_dict(data['traveler']),
            watcher=User.from_dict(data['watcher']),
            distance=data['distance']
        )