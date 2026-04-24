"""
Tests for new API 9.6 features and previously missing methods.
"""
import pytest
from telegram_async.telegram_types import (
    ManagedBotCreated, ManagedBotUpdated, ManagedBotInfo,
    PollOptionExtended, PollExtended, PollOptionAdded, PollOptionDeleted,
    PollAnswerExtended,
    PaidMedia, PaidMediaPhoto, PaidMediaVideo, PaidMediaInfo,
    ChatInviteLink, ChatPermissions, ChatAdministratorRights,
    KeyboardButtonRequestManagedBot, PreparedKeyboardButton
)
from telegram_async.keyboards.reply import ReplyKeyboardButton


class TestManagedBots:
    """Test managed bot types (API 9.6)."""
    
    def test_managed_bot_created(self):
        """Test ManagedBotCreated type."""
        data = {
            'title': 'Test Bot',
            'username': 'test_bot',
            'photo_url': 'https://example.com/photo.jpg'
        }
        bot = ManagedBotCreated.from_dict(data)
        assert bot.title == 'Test Bot'
        assert bot.username == 'test_bot'
        assert bot.photo_url == 'https://example.com/photo.jpg'
    
    def test_managed_bot_updated(self):
        """Test ManagedBotUpdated type."""
        data = {
            'managed_bot_id': 'bot123',
            'new_token': 'new-token-here',
            'date': 1234567890
        }
        updated = ManagedBotUpdated.from_dict(data)
        assert updated.managed_bot_id == 'bot123'
        assert updated.new_token == 'new-token-here'
        assert updated.date == 1234567890
    
    def test_managed_bot_info(self):
        """Test ManagedBotInfo type."""
        data = {
            'managed_bot_id': 'bot123',
            'title': 'My Bot',
            'username': 'my_bot',
            'is_active': True,
            'created_date': 1234567890
        }
        info = ManagedBotInfo.from_dict(data)
        assert info.managed_bot_id == 'bot123'
        assert info.is_active is True
    
    def test_keyboard_button_request_managed_bot(self):
        """Test KeyboardButtonRequestManagedBot."""
        button = KeyboardButtonRequestManagedBot(
            text='Create Bot',
            bot_types=['customer_support', 'moderation']
        )
        data = button.to_dict()
        assert data['text'] == 'Create Bot'
        assert 'bot_types' in data


class TestEnhancedPolls:
    """Test enhanced poll types (API 9.6)."""
    
    def test_poll_option_extended(self):
        """Test PollOptionExtended with API 9.6 fields."""
        data = {
            'text': 'Option 1',
            'voter_count': 10,
            'persistent_id': 'pid123',
            'addition_date': 1234567890
        }
        option = PollOptionExtended.from_dict(data)
        assert option.text == 'Option 1'
        assert option.persistent_id == 'pid123'
        assert option.addition_date == 1234567890
    
    def test_poll_extended(self):
        """Test PollExtended with API 9.6 features."""
        data = {
            'id': 'poll123',
            'question': 'What is your favorite color?',
            'options': [
                {'text': 'Red', 'voter_count': 5},
                {'text': 'Blue', 'voter_count': 10}
            ],
            'total_voter_count': 15,
            'is_closed': False,
            'is_anonymous': True,
            'type': 'regular',
            'correct_option_ids': [0, 1],
            'allows_revoting': True,
            'description': 'Choose your favorite color',
            'shuffle_options': True,
            'allow_adding_options': True,
            'hide_results_until_closes': False
        }
        poll = PollExtended.from_dict(data)
        assert poll.id == 'poll123'
        assert poll.allows_revoting is True
        assert poll.correct_option_ids == [0, 1]
        assert poll.shuffle_options is True
    
    def test_poll_option_added(self):
        """Test PollOptionAdded type."""
        data = {
            'poll_id': 'poll123',
            'option_text': 'New Option',
            'option_persistent_id': 'opt_pid123'
        }
        added = PollOptionAdded.from_dict(data)
        assert added.poll_id == 'poll123'
        assert added.option_text == 'New Option'
    
    def test_poll_option_deleted(self):
        """Test PollOptionDeleted type."""
        data = {
            'poll_id': 'poll123',
            'option_text': 'Deleted Option',
            'option_persistent_id': 'opt_pid456'
        }
        deleted = PollOptionDeleted.from_dict(data)
        assert deleted.poll_id == 'poll123'
        assert deleted.option_text == 'Deleted Option'
    
    def test_poll_answer_extended(self):
        """Test PollAnswerExtended."""
        data = {
            'poll_id': 'poll123',
            'option_ids': [0, 1],
            'option_persistent_ids': ['pid1', 'pid2']
        }
        answer = PollAnswerExtended.from_dict(data)
        assert answer.poll_id == 'poll123'
        assert answer.option_ids == [0, 1]


class TestPaidMedia:
    """Test paid media types (API 9.6)."""
    
    def test_paid_media_photo(self):
        """Test PaidMediaPhoto."""
        data = {
            'type': 'photo',
            'photo': [
                {'file_id': 'photo1', 'width': 800, 'height': 600}
            ]
        }
        media = PaidMediaPhoto.from_dict(data)
        assert media.type == 'photo'
        assert len(media.photo) == 1
    
    def test_paid_media_video(self):
        """Test PaidMediaVideo."""
        data = {
            'type': 'video',
            'width': 1920,
            'height': 1080,
            'duration': 60
        }
        media = PaidMediaVideo.from_dict(data)
        assert media.type == 'video'
        assert media.width == 1920
        assert media.duration == 60
    
    def test_paid_media_info(self):
        """Test PaidMediaInfo."""
        data = {
            'star_count': 100,
            'paid_media': [
                {'type': 'photo'},
                {'type': 'video'}
            ]
        }
        info = PaidMediaInfo.from_dict(data)
        assert info.star_count == 100
        assert len(info.paid_media) == 2


class TestChatInviteLink:
    """Test ChatInviteLink type."""
    
    def test_chat_invite_link_creation(self):
        """Test ChatInviteLink."""
        data = {
            'invite_link': 'https://t.me/+abc123',
            'creator': {'id': 123, 'is_bot': False, 'first_name': 'Test'},
            'creates_join_request': True,
            'is_primary': False,
            'is_revoked': False,
            'name': 'My Link',
            'member_limit': 100
        }
        link = ChatInviteLink.from_dict(data)
        assert link.invite_link == 'https://t.me/+abc123'
        assert link.creates_join_request is True
        assert link.member_limit == 100


class TestChatPermissions:
    """Test ChatPermissions type."""
    
    def test_all_allowed(self):
        """Test ChatPermissions.all_allowed()."""
        perms = ChatPermissions.all_allowed()
        assert perms.can_send_messages is True
        assert perms.can_invite_users is True
        assert perms.can_pin_messages is True
    
    def test_all_denied(self):
        """Test ChatPermissions.all_denied()."""
        perms = ChatPermissions.all_denied()
        assert perms.can_send_messages is False
        assert perms.can_invite_users is False
        assert perms.can_pin_messages is False
    
    def test_to_dict(self):
        """Test ChatPermissions.to_dict()."""
        perms = ChatPermissions(
            can_send_messages=True,
            can_invite_users=False
        )
        data = perms.to_dict()
        assert data['can_send_messages'] is True
        assert data['can_invite_users'] is False


class TestChatAdministratorRights:
    """Test ChatAdministratorRights type."""
    
    def test_default_rights(self):
        """Test default administrator rights."""
        rights = ChatAdministratorRights.default()
        assert rights.is_anonymous is False
        assert rights.can_manage_chat is True
    
    def test_full_rights(self):
        """Test full administrator rights."""
        rights = ChatAdministratorRights.full()
        assert rights.is_anonymous is True
        assert rights.can_manage_chat is True
        assert rights.can_delete_messages is True
        assert rights.can_promote_members is True
    
    def test_to_dict(self):
        """Test rights to_dict()."""
        rights = ChatAdministratorRights(
            is_anonymous=True,
            can_delete_messages=True
        )
        data = rights.to_dict()
        assert data['is_anonymous'] is True
        assert data['can_delete_messages'] is True


class TestPreparedKeyboardButton:
    """Test PreparedKeyboardButton (API 9.6)."""
    
    def test_prepared_keyboard_button(self):
        """Test PreparedKeyboardButton creation."""
        button = PreparedKeyboardButton(
            id='btn1',
            text='Click Me',
            type='text'
        )
        data = button.to_dict()
        assert data['id'] == 'btn1'
        assert data['text'] == 'Click Me'
        assert data['type'] == 'text'
    
    def test_with_managed_bot_request(self):
        """Test button with managed bot request."""
        bot_request = KeyboardButtonRequestManagedBot(
            text='Create Bot'
        )
        button = PreparedKeyboardButton(
            id='btn2',
            text='Create Managed Bot',
            request_managed_bot=bot_request
        )
        data = button.to_dict()
        assert 'request_managed_bot' in data
        assert data['request_managed_bot']['text'] == 'Create Bot'


class TestReplyKeyboardButtonAPI96:
    """Test ReplyKeyboardButton with API 9.6 fields."""
    
    def test_request_managed_bot(self):
        """Test request_managed_bot field."""
        button = ReplyKeyboardButton(
            text='Request Bot',
            request_managed_bot={'text': 'Create Bot'}
        )
        data = button.to_dict()
        assert 'request_managed_bot' in data
        assert data['request_managed_bot']['text'] == 'Create Bot'


class TestMessageAPINewFields:
    """Test Message with new API 9.6 fields."""
    
    def test_message_with_managed_bot_created(self):
        """Test Message with managed_bot_created field."""
        from telegram_async.telegram_types.message import Message
        
        # Just verify the field exists in the class
        assert hasattr(Message, 'managed_bot_created')
        assert hasattr(Message, 'poll_option_added')
        assert hasattr(Message, 'poll_option_deleted')
        assert hasattr(Message, 'reply_to_poll_option_id')
        assert hasattr(Message, 'paid_media')


class TestUserAPI96Fields:
    """Test User with API 9.6 fields."""
    
    def test_user_can_manage_bots(self):
        """Test User.can_manage_bots field."""
        from telegram_async.telegram_types import User
        
        data = {
            'id': 123,
            'is_bot': False,
            'first_name': 'Test',
            'can_manage_bots': True
        }
        user = User.from_dict(data)
        assert user.can_manage_bots is True


class TestReplyParameters:
    """Test ReplyParameters class with API 9.6 poll_option_id."""
    
    def test_reply_parameters_basic(self):
        """Test basic ReplyParameters creation."""
        from telegram_async.telegram_types import ReplyParameters
        
        rp = ReplyParameters(message_id=123, chat_id=-1001234567890)
        assert rp.message_id == 123
        assert rp.chat_id == -1001234567890
        assert rp.poll_option_id is None
    
    def test_reply_parameters_with_poll_option_id(self):
        """Test ReplyParameters with poll_option_id (API 9.6)."""
        from telegram_async.telegram_types import ReplyParameters
        
        rp = ReplyParameters(
            message_id=456,
            chat_id=123456,
            poll_option_id="opt_abc123"
        )
        assert rp.message_id == 456
        assert rp.poll_option_id == "opt_abc123"
        
        data = rp.to_dict()
        assert data['message_id'] == 456
        assert data['poll_option_id'] == "opt_abc123"
    
    def test_reply_parameters_from_dict(self):
        """Test ReplyParameters from_dict with poll_option_id."""
        from telegram_async.telegram_types import ReplyParameters
        
        data = {
            'message_id': 789,
            'chat_id': 111222,
            'allow_sending_without_reply': True,
            'quote': "Reply text",
            'poll_option_id': "opt_xyz789"
        }
        rp = ReplyParameters.from_dict(data)
        assert rp.message_id == 789
        assert rp.poll_option_id == "opt_xyz789"
        assert rp.allow_sending_without_reply is True
        assert rp.quote == "Reply text"


class TestMessageEntityDateTime:
    """Test MessageEntity with date_time type (API 9.6)."""
    
    def test_message_entity_date_time_type(self):
        """Test MessageEntity with date_time type."""
        from telegram_async.telegram_types import MessageEntity
        
        entity = MessageEntity(
            type="date_time",
            offset=0,
            length=10,
            language="en"
        )
        assert entity.type == "date_time"
        assert entity.offset == 0
        assert entity.length == 10
    
    def test_message_entity_to_dict(self):
        """Test MessageEntity to_dict method."""
        from telegram_async.telegram_types import MessageEntity
        
        entity = MessageEntity(
            type="date_time",
            offset=5,
            length=15,
            language="pl"
        )
        data = entity.to_dict()
        assert data['type'] == "date_time"
        assert data['offset'] == 5
        assert data['length'] == 15
        assert data['language'] == "pl"
    
    def test_message_entity_from_dict(self):
        """Test MessageEntity from_dict with date_time type."""
        from telegram_async.telegram_types import MessageEntity
        
        data = {
            'type': 'date_time',
            'offset': 10,
            'length': 20,
            'language': 'uk'
        }
        entity = MessageEntity.from_dict(data)
        assert entity.type == "date_time"
        assert entity.offset == 10
        assert entity.length == 20
        assert entity.language == "uk"
