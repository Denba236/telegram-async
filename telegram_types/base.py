from dataclasses import dataclass
from typing import Optional, Dict, Any
import json


@dataclass
class TelegramObject:
    """Base class for all Telegram API objects"""

    def to_dict(self) -> Dict[str, Any]:
        """Converts object to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                elif isinstance(value, list):
                    result[key] = [
                        v.to_dict() if hasattr(v, 'to_dict') else v
                        for v in value
                    ]
                else:
                    result[key] = value
        return result

    def to_json(self) -> str:
        """Converts object to JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TelegramObject':
        """Creates an object from a dictionary"""
        return cls(**data)


@dataclass
class File(TelegramObject):
    """Base class for files"""
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> 'File':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            file_size=data.get('file_size'),
            file_path=data.get('file_path')
        )
