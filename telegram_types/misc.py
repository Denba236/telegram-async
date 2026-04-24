from dataclasses import dataclass
from typing import Optional, Dict, List, Any

from .user import User
from .media import PhotoSize, Animation
from .message import MessageEntity
from .base import File


@dataclass
class Contact:
    """Contact"""
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        return cls(
            phone_number=data['phone_number'],
            first_name=data['first_name'],
            last_name=data.get('last_name'),
            user_id=data.get('user_id'),
            vcard=data.get('vcard')
        )


@dataclass
class Dice:
    """Dice game"""
    emoji: str  # '🎲', '🎯', '🏀', '⚽', '🎳', '🎰'
    value: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'Dice':
        return cls(
            emoji=data['emoji'],
            value=data['value']
        )


@dataclass
class Location:
    """Location"""
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
class Venue:
    """Venue"""
    location: Location
    title: str
    address: str
    foursquare_id: Optional[str] = None
    foursquare_type: Optional[str] = None
    google_place_id: Optional[str] = None
    google_place_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Venue':
        return cls(
            location=Location.from_dict(data['location']),
            title=data['title'],
            address=data['address'],
            foursquare_id=data.get('foursquare_id'),
            foursquare_type=data.get('foursquare_type'),
            google_place_id=data.get('google_place_id'),
            google_place_type=data.get('google_place_type')
        )


@dataclass
class PollOption:
    """Poll option"""
    text: str
    voter_count: int
    persistent_id: Optional[str] = None  # API 9.6
    added_by_user: Optional[User] = None  # API 9.6
    added_by_chat: Optional[Any] = None  # API 9.6 (Chat)
    addition_date: Optional[int] = None  # API 9.6

    @classmethod
    def from_dict(cls, data: Dict) -> 'PollOption':
        from .user import User, Chat
        return cls(
            text=data['text'],
            voter_count=data['voter_count'],
            persistent_id=data.get('persistent_id'),
            added_by_user=User.from_dict(data['added_by_user']) if 'added_by_user' in data else None,
            added_by_chat=Chat.from_dict(data['added_by_chat']) if 'added_by_chat' in data else None,
            addition_date=data.get('addition_date')
        )


@dataclass
class Poll:
    """Poll"""
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str  # 'regular', 'quiz'
    allows_multiple_answers: bool
    correct_option_id: Optional[int] = None  # Deprecated in API 9.6
    correct_option_ids: Optional[List[int]] = None  # API 9.6
    explanation: Optional[str] = None
    explanation_entities: Optional[List[MessageEntity]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None
    # API 9.6
    allows_revoting: Optional[bool] = None
    description: Optional[str] = None
    description_entities: Optional[List[MessageEntity]] = None
    shuffle_options: Optional[bool] = None
    allow_adding_options: Optional[bool] = None
    hide_results_until_closes: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Poll':
        return cls(
            id=data['id'],
            question=data['question'],
            options=[PollOption.from_dict(o) for o in data['options']],
            total_voter_count=data['total_voter_count'],
            is_closed=data['is_closed'],
            is_anonymous=data['is_anonymous'],
            type=data['type'],
            allows_multiple_answers=data['allows_multiple_answers'],
            correct_option_id=data.get('correct_option_id'),
            correct_option_ids=data.get('correct_option_ids'),
            explanation=data.get('explanation'),
            explanation_entities=[MessageEntity.from_dict(e) for e in
                                  data['explanation_entities']] if 'explanation_entities' in data else None,
            open_period=data.get('open_period'),
            close_date=data.get('close_date'),
            allows_revoting=data.get('allows_revoting'),
            description=data.get('description'),
            description_entities=[MessageEntity.from_dict(e) for e in
                                  data['description_entities']] if 'description_entities' in data else None,
            shuffle_options=data.get('shuffle_options'),
            allow_adding_options=data.get('allow_adding_options'),
            hide_results_until_closes=data.get('hide_results_until_closes')
        )


@dataclass
class Game:
    """Game"""
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Game':
        return cls(
            title=data['title'],
            description=data['description'],
            photo=[PhotoSize.from_dict(p) for p in data['photo']],
            text=data.get('text'),
            text_entities=[MessageEntity.from_dict(e) for e in
                           data['text_entities']] if 'text_entities' in data else None,
            animation=Animation.from_dict(data['animation']) if 'animation' in data else None
        )
