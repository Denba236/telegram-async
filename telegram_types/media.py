from dataclasses import dataclass
from typing import Optional, Dict, List

from .base import File


@dataclass
class PhotoSize(File):
    """Rozmiar zdjęcia"""
    width: int
    height: int

    @classmethod
    def from_dict(cls, data: Dict) -> 'PhotoSize':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            width=data['width'],
            height=data['height']
        )


@dataclass
class Animation(File):
    """Animacja (GIF)"""
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Animation':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            width=data['width'],
            height=data['height'],
            duration=data['duration'],
            thumb=PhotoSize.from_dict(data['thumb']) if 'thumb' in data else None,
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type')
        )


@dataclass
class Audio(File):
    """Plik audio"""
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    thumb: Optional[PhotoSize] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Audio':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            duration=data['duration'],
            performer=data.get('performer'),
            title=data.get('title'),
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            thumb=PhotoSize.from_dict(data['thumb']) if 'thumb' in data else None
        )


@dataclass
class Document(File):
    """Dokument"""
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    thumb: Optional[PhotoSize] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Document':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            thumb=PhotoSize.from_dict(data['thumb']) if 'thumb' in data else None
        )


@dataclass
class Video(File):
    """Plik wideo"""
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Video':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            width=data['width'],
            height=data['height'],
            duration=data['duration'],
            thumb=PhotoSize.from_dict(data['thumb']) if 'thumb' in data else None,
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type')
        )


@dataclass
class VideoNote(File):
    """Okrągłe wideo"""
    length: int
    duration: int
    thumb: Optional[PhotoSize] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoNote':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            length=data['length'],
            duration=data['duration'],
            thumb=PhotoSize.from_dict(data['thumb']) if 'thumb' in data else None
        )


@dataclass
class Voice(File):
    """Wiadomość głosowa"""
    duration: int
    mime_type: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Voice':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            duration=data['duration'],
            mime_type=data.get('mime_type')
        )


@dataclass
class MaskPosition:
    """Pozycja maski na twarzy"""
    point: str  # 'forehead', 'eyes', 'mouth', 'chin'
    x_shift: float
    y_shift: float
    scale: float

    @classmethod
    def from_dict(cls, data: Dict) -> 'MaskPosition':
        return cls(
            point=data['point'],
            x_shift=data['x_shift'],
            y_shift=data['y_shift'],
            scale=data['scale']
        )


@dataclass
class Sticker(File):
    """Naklejka"""
    type: str  # 'regular', 'mask', 'custom_emoji'
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: Optional[PhotoSize] = None
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[File] = None
    mask_position: Optional[MaskPosition] = None
    custom_emoji_id: Optional[str] = None
    needs_repainting: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Sticker':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path'),
            type=data['type'],
            width=data['width'],
            height=data['height'],
            is_animated=data['is_animated'],
            is_video=data['is_video'],
            thumb=PhotoSize.from_dict(data['thumb']) if 'thumb' in data else None,
            emoji=data.get('emoji'),
            set_name=data.get('set_name'),
            premium_animation=File.from_dict(data['premium_animation']) if 'premium_animation' in data else None,
            mask_position=MaskPosition.from_dict(data['mask_position']) if 'mask_position' in data else None,
            custom_emoji_id=data.get('custom_emoji_id'),
            needs_repainting=data.get('needs_repainting')
        )