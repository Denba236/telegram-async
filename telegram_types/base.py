from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class File:
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