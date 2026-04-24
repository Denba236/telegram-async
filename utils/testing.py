"""
Testing utilities - Mock Bot and Client for unit testing handlers
"""
import asyncio
from typing import Dict, Any, Optional, List, Callable
from unittest.mock import AsyncMock, MagicMock
from dataclasses import dataclass, field


@dataclass
class SentMessage:
    """Represents a sent message for testing."""
    chat_id: Any
    text: str
    parse_mode: Optional[str] = None
    reply_markup: Optional[Dict] = None
    disable_notification: bool = False
    reply_to_message_id: Optional[int] = None


@dataclass
class SentPhoto:
    """Represents a sent photo for testing."""
    chat_id: Any
    photo: Any
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    reply_markup: Optional[Dict] = None


class MockBot:
    """
    Mock bot for testing handlers without making real API calls.
    
    Usage:
        bot = MockBot()
        
        # Call your handler
        await handler(bot, update)
        
        # Assert on what was sent
        assert len(bot.sent_messages) == 1
        assert bot.sent_messages[0].text == "Expected response"
        assert bot.sent_messages[0].chat_id == 123
    """
    
    def __init__(self):
        self.sent_messages: List[SentMessage] = []
        self.sent_photos: List[SentPhoto] = []
        self.edited_messages: List[Dict] = []
        self.deleted_messages: List[Dict] = []
        self.callback_answers: List[Dict] = []
        self.chat_actions: List[Dict] = []
        
        # Mock responses for API calls
        self._mock_responses: Dict[str, Any] = {}
        self._me_response = {
            'id': 123456789,
            'is_bot': True,
            'first_name': 'Test Bot',
            'username': 'test_bot'
        }
    
    def set_me_response(self, user_info: Dict[str, Any]):
        """Set what the bot returns for get_me()."""
        self._me_response = user_info
    
    def add_mock_response(self, method: str, response: Any):
        """Add a mock response for a specific method."""
        self._mock_responses[method] = response
    
    async def get_me(self) -> Dict[str, Any]:
        """Mock get_me()."""
        return self._me_response
    
    async def send_message(
        self,
        chat_id: Any,
        text: str,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict] = None,
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Mock send_message."""
        message = SentMessage(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id
        )
        self.sent_messages.append(message)
        
        # Return a fake message object
        return {
            'message_id': len(self.sent_messages),
            'from': self._me_response,
            'chat': {'id': chat_id},
            'date': 1234567890,
            'text': text
        }
    
    async def send_photo(
        self,
        chat_id: Any,
        photo: Any,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Mock send_photo."""
        photo_obj = SentPhoto(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
        self.sent_photos.append(photo_obj)
        
        return {
            'message_id': len(self.sent_messages),
            'from': self._me_response,
            'chat': {'id': chat_id},
            'date': 1234567890,
            'photo': [{'file_id': 'AgACAgIAAxkBAAIB'}]
        }
    
    async def edit_message_text(
        self,
        text: str,
        chat_id: Optional[Any] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        reply_markup: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """Mock edit_message_text."""
        edit = {
            'chat_id': chat_id,
            'message_id': message_id,
            'inline_message_id': inline_message_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup
        }
        self.edited_messages.append(edit)
        
        return {
            'message_id': message_id or 0,
            'text': text
        }
    
    async def delete_message(
        self,
        chat_id: Any,
        message_id: int,
        **kwargs
    ) -> bool:
        """Mock delete_message."""
        self.deleted_messages.append({
            'chat_id': chat_id,
            'message_id': message_id
        })
        return True
    
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
        **kwargs
    ) -> bool:
        """Mock answer_callback_query."""
        self.callback_answers.append({
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert
        })
        return True
    
    async def send_chat_action(
        self,
        chat_id: Any,
        action: str,
        **kwargs
    ) -> bool:
        """Mock send_chat_action."""
        self.chat_actions.append({
            'chat_id': chat_id,
            'action': action
        })
        return True
    
    async def _request(self, method: str, data: Optional[Dict] = None, **kwargs) -> Any:
        """Generic mock request."""
        if method in self._mock_responses:
            return self._mock_responses[method]
        return {}
    
    def clear(self):
        """Clear all recorded actions."""
        self.sent_messages.clear()
        self.sent_photos.clear()
        self.edited_messages.clear()
        self.deleted_messages.clear()
        self.callback_answers.clear()
        self.chat_actions.clear()
    
    def assert_sent_message_count(self, count: int):
        """Assert number of sent messages."""
        assert len(self.sent_messages) == count, \
            f"Expected {count} sent messages, got {len(self.sent_messages)}"
    
    def assert_sent_text(self, text: str, index: int = 0):
        """Assert sent message text."""
        assert index < len(self.sent_messages), \
            f"No message at index {index}"
        assert self.sent_messages[index].text == text, \
            f"Expected text '{text}', got '{self.sent_messages[index].text}'"
    
    def assert_sent_to_chat(self, chat_id: Any, index: int = 0):
        """Assert message was sent to specific chat."""
        assert index < len(self.sent_messages), \
            f"No message at index {index}"
        assert self.sent_messages[index].chat_id == chat_id, \
            f"Expected chat_id {chat_id}, got {self.sent_messages[index].chat_id}"
    
    def assert_callback_answered(self, text: Optional[str] = None, index: int = 0):
        """Assert callback was answered."""
        assert index < len(self.callback_answers), \
            f"No callback answer at index {index}"
        if text is not None:
            assert self.callback_answers[index]['text'] == text, \
                f"Expected callback text '{text}', got '{self.callback_answers[index]['text']}'"


class MockContext:
    """
    Mock context for testing handlers.
    
    Usage:
        context = MockContext(user_id=123, chat_id=456, text="/start")
        await handler(bot, context)
    """
    
    def __init__(
        self,
        user_id: int = 123,
        chat_id: int = 456,
        text: str = "",
        update: Optional[Dict] = None,
        callback_data: Optional[str] = None,
        message: Optional[Dict] = None
    ):
        self.user_id = user_id
        self.chat_id = chat_id
        self.text = text
        self.update = update or {}
        self.callback_data = callback_data
        self.message = message or {}
        
        # Track method calls
        self.replied = []
        self.edited = []
        self.deleted = []
        self.callback_answered = []
    
    async def reply(self, text: str, **kwargs):
        """Mock reply."""
        self.replied.append({'text': text, **kwargs})
        return {'message_id': 1, 'text': text}
    
    async def reply_text(self, text: str, **kwargs):
        """Mock reply_text."""
        return await self.reply(text, **kwargs)
    
    async def edit_message(self, text: str, **kwargs):
        """Mock edit_message."""
        self.edited.append({'text': text, **kwargs})
        return {'message_id': 1, 'text': text}
    
    async def delete_message(self):
        """Mock delete_message."""
        self.deleted.append({'chat_id': self.chat_id})
        return True
    
    async def answer_callback(self, text: Optional[str] = None, **kwargs):
        """Mock answer_callback."""
        self.callback_answered.append({'text': text, **kwargs})
        return True
    
    def assert_replied(self, text: Optional[str] = None, count: int = 1):
        """Assert context replied."""
        assert len(self.replied) == count, \
            f"Expected {count} replies, got {len(self.replied)}"
        if text is not None:
            assert any(r['text'] == text for r in self.replied), \
                f"Expected reply text '{text}', got {[r['text'] for r in self.replied]}"
    
    def assert_edited(self, text: Optional[str] = None):
        """Assert context edited message."""
        assert len(self.edited) > 0, "Expected edit but got none"
        if text is not None:
            assert any(e['text'] == text for e in self.edited), \
                f"Expected edit text '{text}', got {[e['text'] for e in self.edited]}"


async def run_handler_test(handler_func, bot: MockBot, context: MockContext):
    """
    Helper to run a handler test.
    
    Usage:
        bot = MockBot()
        ctx = MockContext(text="/start")
        await run_handler_test(my_handler, bot, ctx)
        
        bot.assert_sent_text("Welcome!")
    """
    await handler_func(bot, context)
