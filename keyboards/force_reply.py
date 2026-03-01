from typing import Dict, Any, Optional


class ForceReply:
    def __init__(self, selective: bool = True, input_field_placeholder: Optional[str] = None):
        self.selective = selective
        self.input_field_placeholder = input_field_placeholder

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'force_reply': True,
            'selective': self.selective
        }
        if self.input_field_placeholder:
            result['input_field_placeholder'] = self.input_field_placeholder
        return result