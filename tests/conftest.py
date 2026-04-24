"""
Pytest configuration for telegram_async tests.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_bot():
    """Create a mock Bot instance for testing."""
    from telegram_async.client.bot import Bot
    
    bot = MagicMock(spec=Bot)
    bot.token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    bot.session = AsyncMock()
    return bot


@pytest.fixture
def mock_context():
    """Create a mock Context for testing handlers."""
    from telegram_async.dispatcher.context import Context
    
    context = MagicMock(spec=Context)
    context.chat_id = 123456789
    context.user_id = 987654321
    context.text = "/start"
    context.reply = AsyncMock()
    context.answer = AsyncMock()
    return context


@pytest.fixture
def mock_update():
    """Create a mock Update object."""
    from telegram_async.telegram_types.update import Update
    from telegram_async.telegram_types.message import Message
    from telegram_async.telegram_types.user import User
    
    update = MagicMock(spec=Update)
    update.update_id = 1
    update.message = MagicMock(spec=Message)
    update.message.message_id = 1
    update.message.from_user = MagicMock(spec=User)
    update.message.from_user.id = 123456789
    update.message.chat.id = 123456789
    update.message.text = "/start"
    return update
