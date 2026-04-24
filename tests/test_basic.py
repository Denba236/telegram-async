"""
Basic tests for telegram_async package.
"""
import pytest
from telegram_async import Bot, Dispatcher, Router, Context


class TestPackageImports:
    """Test that all package imports work correctly."""
    
    def test_bot_import(self):
        """Test Bot class import."""
        assert Bot is not None
    
    def test_dispatcher_import(self):
        """Test Dispatcher class import."""
        assert Dispatcher is not None
    
    def test_router_import(self):
        """Test Router class import."""
        assert Router is not None
    
    def test_context_import(self):
        """Test Context class import."""
        assert Context is not None


class TestBot:
    """Test Bot class functionality."""
    
    def test_bot_token_validation(self):
        """Test Bot token validation."""
        # Valid token format
        valid_token = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        bot = Bot(token=valid_token)
        assert bot is not None
    
    def test_bot_invalid_token_format(self):
        """Test Bot rejects invalid token format."""
        with pytest.raises(ValueError):
            Bot(token="invalid-token")


class TestFilters:
    """Test filter system."""
    
    def test_text_filter(self):
        """Test text filter creation."""
        from telegram_async.filters.base import Text
        text_filter = Text("hello")
        assert text_filter is not None
    
    def test_command_filter(self):
        """Test command filter creation."""
        from telegram_async.filters import Command
        cmd_filter = Command("start")
        assert cmd_filter is not None


class TestFSM:
    """Test FSM functionality."""
    
    def test_state_creation(self):
        """Test State creation."""
        from telegram_async.fsm import State
        state = State("test_state")
        assert state is not None
    
    def test_states_group(self):
        """Test StatesGroup creation."""
        from telegram_async.fsm import StatesGroup, State
        
        class MyStates(StatesGroup):
            WAITING = State("waiting")
            PROCESSING = State("processing")
        
        assert hasattr(MyStates, 'WAITING')
        assert hasattr(MyStates, 'PROCESSING')


class TestKeyboards:
    """Test keyboard builders."""
    
    def test_inline_keyboard(self):
        """Test InlineKeyboardMarkup creation."""
        from telegram_async.keyboards.inline import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup()
        assert keyboard is not None
        
    def test_reply_keyboard(self):
        """Test ReplyKeyboardMarkup creation."""
        from telegram_async.keyboards.reply import ReplyKeyboardMarkup
        
        keyboard = ReplyKeyboardMarkup()
        assert keyboard is not None
