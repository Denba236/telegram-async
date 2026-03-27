from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class WebAppData:
    """Web App data"""
    data: str
    button_text: str

    @classmethod
    def from_dict(cls, data: Dict) -> 'WebAppData':
        return cls(
            data=data['data'],
            button_text=data['button_text']
        )
