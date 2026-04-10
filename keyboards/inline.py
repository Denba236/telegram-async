from typing import List, Dict, Any, Optional, Literal


class InlineKeyboardButton:
    """
    Кнопка inline клавиатуры (InlineKeyboardButton в API Telegram)
    
    API 9.4+: поддерживает стилизацию (цвет) кнопки через параметр style
    """
    
    # Допустимые стили (цвета) для кнопок - API 9.4+
    STYLE_PRIMARY = "primary"    # Синий цвет
    STYLE_SUCCESS = "success"    # Зеленый цвет
    STYLE_DANGER = "danger"      # Красный цвет
    
    def __init__(
            self,
            text: str,
            callback_data: Optional[str] = None,
            url: Optional[str] = None,
            login_url: Optional[Dict] = None,
            switch_inline_query: Optional[str] = None,
            switch_inline_query_current_chat: Optional[str] = None,
            callback_game: Optional[Dict] = None,
            pay: bool = False,
            web_app: Optional[Dict] = None,
            icon_custom_emoji_id: Optional[str] = None,  # API 9.5 - custom emoji icon
            style: Optional[Literal["primary", "success", "danger"]] = None  # API 9.4+ - цвет кнопки
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.login_url = login_url
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay
        self.web_app = web_app
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style  # Стиль (цвет) кнопки: primary/success/danger

    def to_dict(self) -> Dict[str, Any]:
        data = {'text': self.text}
        if self.callback_data is not None:
            data['callback_data'] = self.callback_data
        if self.url is not None:
            data['url'] = self.url
        if self.login_url is not None:
            data['login_url'] = self.login_url
        if self.switch_inline_query is not None:
            data['switch_inline_query'] = self.switch_inline_query
        if self.switch_inline_query_current_chat is not None:
            data['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        if self.callback_game is not None:
            data['callback_game'] = self.callback_game
        if self.pay:
            data['pay'] = True
        if self.web_app is not None:
            data['web_app'] = self.web_app
        if self.icon_custom_emoji_id is not None:
            data['icon_custom_emoji_id'] = self.icon_custom_emoji_id  # API 9.5
        if self.style is not None:
            data['style'] = self.style  # API 9.4+ - цвет кнопки
        return data


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: Optional[List[List[InlineKeyboardButton]]] = None):
        self.inline_keyboard = inline_keyboard or []

    @classmethod
    def row(cls, *buttons: InlineKeyboardButton) -> 'InlineKeyboardMarkup':
        """Creates a keyboard with a single row"""
        return cls([list(buttons)])

    def add(self, *buttons: InlineKeyboardButton) -> 'InlineKeyboardMarkup':
        """Adds a new row with buttons"""
        self.inline_keyboard.append(list(buttons))
        return self

    def to_dict(self) -> Dict[str, List[List[Dict]]]:
        return {
            'inline_keyboard': [
                [btn.to_dict() for btn in row]
                for row in self.inline_keyboard
            ]
        }
