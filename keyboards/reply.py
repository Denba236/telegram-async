from typing import List, Dict, Any, Optional, Literal


class ReplyKeyboardButton:
    """
    Кнопка reply клавиатуры (KeyboardButton в API Telegram)
    
    API 9.4+: поддерживает стилизацию (цвет) кнопки через параметр style
    """
    
    # Допустимые стили (цвета) для кнопок - API 9.4+
    STYLE_PRIMARY = "primary"    # Синий цвет
    STYLE_SUCCESS = "success"    # Зеленый цвет
    STYLE_DANGER = "danger"      # Красный цвет
    
    def __init__(
            self,
            text: str,
            request_contact: bool = False,
            request_location: bool = False,
            request_poll: Optional[Dict] = None,
            web_app: Optional[Dict] = None,
            request_user: Optional[Dict] = None,
            request_chat: Optional[Dict] = None,
            request_managed_bot: Optional[Dict] = None,  # API 9.6
            icon_custom_emoji_id: Optional[str] = None,  # API 9.5 - custom emoji icon for BottomButton
            style: Optional[Literal["primary", "success", "danger"]] = None  # API 9.4+ - цвет кнопки
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll
        self.web_app = web_app
        self.request_user = request_user
        self.request_chat = request_chat
        self.request_managed_bot = request_managed_bot  # API 9.6
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style  # Стиль (цвет) кнопки: primary/success/danger

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
        if self.request_user:
            data['request_user'] = self.request_user
        if self.request_chat:
            data['request_chat'] = self.request_chat
        if self.request_managed_bot:
            data['request_managed_bot'] = self.request_managed_bot  # API 9.6
        if self.icon_custom_emoji_id:
            data['icon_custom_emoji_id'] = self.icon_custom_emoji_id  # API 9.5
        if self.style:
            data['style'] = self.style  # API 9.4+ - цвет кнопки
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
        """Creates a keyboard with a single row (for simple text buttons)"""
        keyboard = [[ReplyKeyboardButton(text) for text in buttons]]
        return cls(keyboard)

    def add(self, *buttons: str) -> 'ReplyKeyboardMarkup':
        """Adds a new row with text buttons"""
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
    """Class to remove the keyboard"""

    @staticmethod
    def to_dict() -> Dict[str, Any]:
        return {'remove_keyboard': True}
