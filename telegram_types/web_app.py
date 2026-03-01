from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class WebAppData:
    """Dane z Web App"""
    data: str
    button_text: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'WebAppData':
        return cls(
            data=data['data'],
            button_text=data['button_text']
        )