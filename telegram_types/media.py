from dataclasses import dataclass
from typing import Optional, Dict, List

from .base import File


class PhotoSize(File):
    """Rozmiar zdjęcia"""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int,
                 file_size: Optional[int] = None, file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.width = width
        self.height = height

    @classmethod
    def from_dict(cls, data: Dict) -> 'PhotoSize':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


class Animation(File):
    """Animacja (GIF)"""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int,
                 thumb: Optional['PhotoSize'] = None, file_name: Optional[str] = None,
                 mime_type: Optional[str] = None, file_size: Optional[int] = None,
                 file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type

    @classmethod
    def from_dict(cls, data: Dict) -> 'Animation':
        thumb = None
        if 'thumb' in data:
            from .media import PhotoSize
            thumb = PhotoSize.from_dict(data['thumb'])

        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            duration=data['duration'],
            thumb=thumb,
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


class Audio(File):
    """Plik audio"""

    def __init__(self, file_id: str, file_unique_id: str, duration: int,
                 performer: Optional[str] = None, title: Optional[str] = None,
                 file_name: Optional[str] = None, mime_type: Optional[str] = None,
                 thumb: Optional['PhotoSize'] = None, file_size: Optional[int] = None,
                 file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.duration = duration
        self.performer = performer
        self.title = title
        self.file_name = file_name
        self.mime_type = mime_type
        self.thumb = thumb

    @classmethod
    def from_dict(cls, data: Dict) -> 'Audio':
        thumb = None
        if 'thumb' in data:
            from .media import PhotoSize
            thumb = PhotoSize.from_dict(data['thumb'])

        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            performer=data.get('performer'),
            title=data.get('title'),
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            thumb=thumb,
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


class Document(File):
    """Dokument"""

    def __init__(self, file_id: str, file_unique_id: str,
                 file_name: Optional[str] = None, mime_type: Optional[str] = None,
                 thumb: Optional['PhotoSize'] = None, file_size: Optional[int] = None,
                 file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.file_name = file_name
        self.mime_type = mime_type
        self.thumb = thumb

    @classmethod
    def from_dict(cls, data: Dict) -> 'Document':
        thumb = None
        if 'thumb' in data:
            from .media import PhotoSize
            thumb = PhotoSize.from_dict(data['thumb'])

        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            thumb=thumb,
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


class Video(File):
    """Plik wideo"""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int,
                 thumb: Optional['PhotoSize'] = None, file_name: Optional[str] = None,
                 mime_type: Optional[str] = None, file_size: Optional[int] = None,
                 file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type

    @classmethod
    def from_dict(cls, data: Dict) -> 'Video':
        thumb = None
        if 'thumb' in data:
            from .media import PhotoSize
            thumb = PhotoSize.from_dict(data['thumb'])

        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            duration=data['duration'],
            thumb=thumb,
            file_name=data.get('file_name'),
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


class VideoNote(File):
    """Okrągłe wideo"""

    def __init__(self, file_id: str, file_unique_id: str, length: int, duration: int,
                 thumb: Optional['PhotoSize'] = None, file_size: Optional[int] = None,
                 file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.length = length
        self.duration = duration
        self.thumb = thumb

    @classmethod
    def from_dict(cls, data: Dict) -> 'VideoNote':
        thumb = None
        if 'thumb' in data:
            from .media import PhotoSize
            thumb = PhotoSize.from_dict(data['thumb'])

        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            length=data['length'],
            duration=data['duration'],
            thumb=thumb,
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


class Voice(File):
    """Wiadomość głosowa"""

    def __init__(self, file_id: str, file_unique_id: str, duration: int,
                 mime_type: Optional[str] = None, file_size: Optional[int] = None,
                 file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.duration = duration
        self.mime_type = mime_type

    @classmethod
    def from_dict(cls, data: Dict) -> 'Voice':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            duration=data['duration'],
            mime_type=data.get('mime_type'),
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )


@dataclass
class MaskPosition:
    """Pozycja maski na twarzy"""
    point: str
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


class Sticker(File):
    """Naklejka"""

    def __init__(self, file_id: str, file_unique_id: str, type: str, width: int, height: int,
                 is_animated: bool, is_video: bool, thumb: Optional['PhotoSize'] = None,
                 emoji: Optional[str] = None, set_name: Optional[str] = None,
                 premium_animation: Optional['File'] = None,
                 mask_position: Optional[MaskPosition] = None,
                 custom_emoji_id: Optional[str] = None,
                 needs_repainting: Optional[bool] = None,
                 file_size: Optional[int] = None, file_path: Optional[str] = None):
        super().__init__(file_id, file_unique_id, file_size, file_path)
        self.type = type
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.is_video = is_video
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.premium_animation = premium_animation
        self.mask_position = mask_position
        self.custom_emoji_id = custom_emoji_id
        self.needs_repainting = needs_repainting

    @classmethod
    def from_dict(cls, data: Dict) -> 'Sticker':
        from .base import File

        thumb = None
        if 'thumb' in data:
            from .media import PhotoSize
            thumb = PhotoSize.from_dict(data['thumb'])

        premium_animation = None
        if 'premium_animation' in data:
            premium_animation = File.from_dict(data['premium_animation'])

        mask_position = None
        if 'mask_position' in data:
            mask_position = MaskPosition.from_dict(data['mask_position'])

        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            type=data['type'],
            width=data['width'],
            height=data['height'],
            is_animated=data['is_animated'],
            is_video=data['is_video'],
            thumb=thumb,
            emoji=data.get('emoji'),
            set_name=data.get('set_name'),
            premium_animation=premium_animation,
            mask_position=mask_position,
            custom_emoji_id=data.get('custom_emoji_id'),
            needs_repainting=data.get('needs_repainting'),
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )