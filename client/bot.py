import re
from telegram_async.client import TelegramClient


class Bot(TelegramClient):
    """
    Główna klasa bota Telegram

    Przykład:
        bot = Bot("TOKEN")
        await bot.send_message(123456, "Hello!")
    """

    @staticmethod
    def validate_token(token: str) -> bool:
        """Sprawdza czy token ma prawidłowy format"""
        pattern = r'^\d+:[\w-]+$'
        return bool(re.match(pattern, token))

    def __init__(self, token: str):
        if not self.validate_token(token):
            raise ValueError(
                "Nieprawidłowy format tokena! "
                "Token powinien wyglądać tak: 123456789:ABCdefGHIjklmNOPqrstUVWXYZ"
            )
        super().__init__(token)