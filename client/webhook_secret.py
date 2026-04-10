"""
Webhook secret token validation middleware
"""
import logging
from typing import Optional
from aiohttp import web

from ..exceptions import TelegramError

logger = logging.getLogger(__name__)


class SecretTokenValidation:
    """
    Validates X-Telegram-Bot-Api-Secret-Token header on incoming webhook requests.
    
    Usage:
        validator = SecretTokenValidation("your-secret-token")
        server = WebhookServer(dispatcher, bot)
        server.add_middleware(validator.validate)
    """

    def __init__(self, secret_token: str, strict: bool = True):
        """
        Args:
            secret_token: The secret token set via set_webhook(secret_token=...)
            strict: If True, reject requests without the header (default: True)
        """
        self.secret_token = secret_token
        self.strict = strict

    async def validate(self, request: web.Request, handler) -> web.Response:
        """
        Middleware to validate the secret token header.
        """
        if request.method != 'POST':
            return await handler(request)

        token = request.headers.get('X-Telegram-Bot-Api-Secret-Token')

        if not token:
            if self.strict:
                logger.warning("Missing secret token header")
                return web.Response(status=403, text="Forbidden: missing secret token")
            return await handler(request)

        if token != self.secret_token:
            logger.warning("Invalid secret token received")
            return web.Response(status=403, text="Forbidden: invalid secret token")

        return await handler(request)
