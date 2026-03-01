from dataclasses import dataclass
from typing import Optional, Dict, Any
import json


@dataclass
class TelegramObject:
    """Klasa bazowa dla wszystkich obiektów Telegram API"""

    def to_dict(self) -> Dict[str, Any]:
        """Konwertuje obiekt do słownika"""
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
        """Konwertuje obiekt do JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TelegramObject':
        """Tworzy obiekt ze słownika"""
        return cls(**data)


@dataclass
class File(TelegramObject):  # Teraz File dziedziczy po TelegramObject
    """Bazowa klasa dla plików"""
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