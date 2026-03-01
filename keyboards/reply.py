from typing import List, Dict, Any, Optional


class ReplyKeyboardButton:
    def __init__(
            self,
            text: str,
            request_contact: bool = False,
            request_location: bool = False,
            request_poll: Optional[Dict] = None,
            web_app: Optional[Dict] = None
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
        self.web_app = web_app

    def to_dict(self) -> Dict[str, Any]:
        data = {'text': self.text}
        if self.request_contact:
            data['request_contact'] = True
        if self.request_location:
            data['request_location'] = True
        if self.request_poll:
            data['request_poll'] = self.request_poll
        if self.web_app:
            data['web_app'] = self.web_app
        return data


class ReplyKeyboardMarkup:
    def __init__(
            self,
            keyboard: Optional[List[List[ReplyKeyboardButton]]] = None,
            resize_keyboard: bool = True,
            one_time_keyboard: bool = False,
            input_field_placeholder: Optional[str] = None,
            selective: bool = False
    ):
        self.keyboard = keyboard or []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.input_field_placeholder = input_field_placeholder
        self.selective = selective

    @classmethod
    def row(cls, *buttons: str) -> 'ReplyKeyboardMarkup':
        """Tworzy klawiaturę z jednym wierszem (dla prostych przycisków tekstowych)"""
        keyboard = [[ReplyKeyboardButton(text) for text in buttons]]
        return cls(keyboard)

    def add(self, *buttons: str) -> 'ReplyKeyboardMarkup':
        """Dodaje nowy wiersz z przyciskami tekstowymi"""
        self.keyboard.append([ReplyKeyboardButton(text) for text in buttons])
        return self

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'keyboard': [
                [btn.to_dict() for btn in row]
                for row in self.keyboard
            ],
            'resize_keyboard': self.resize_keyboard,
            'one_time_keyboard': self.one_time_keyboard,
            'selective': self.selective
        }
        if self.input_field_placeholder:
            result['input_field_placeholder'] = self.input_field_placeholder
        return result


class ReplyKeyboardRemove:
    """Klasa do usuwania klawiatury"""

    @staticmethod
    def to_dict() -> Dict[str, Any]:
        return {'remove_keyboard': True}