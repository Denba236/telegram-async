import re
from .base import TelegramClient


class Bot(TelegramClient):
    """
    Main Telegram Bot class

    Example:
        bot = Bot("TOKEN")
        await bot.send_message(123456, "Hello!")
    """

    @staticmethod
    def validate_token(token: str) -> bool:
        """Validates if the token has the correct format"""
        pattern = r'^\d+:[\w-]+$'
        return bool(re.match(pattern, token))

    def __init__(self, token: str, **kwargs):
        if not self.validate_token(token):
            raise ValueError(
                "Invalid token format! "
                "Token should look like: 123456789:ABCdefGHIjklmNOPqrstUVWXYZ"
            )
        super().__init__(token, **kwargs)
