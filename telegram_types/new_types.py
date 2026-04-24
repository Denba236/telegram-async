"""
Additional Telegram Bot API types for API 9.5+
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Union


# ==================== Bot Commands ====================

@dataclass
class BotCommand:
    """Represents a bot command."""
    command: str  # 1-32 chars, lowercase, no @ for default
    description: str  # 1-256 chars
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BotCommand':
        return cls(
            command=data['command'],
            description=data['description']
        )


@dataclass
class BotCommandScope:
    """Scope for bot commands."""
    type: str  # default, all_chat_administrators, all_group_administrators, chat, chat_administrators, chat_member
    chat_id: Optional[Union[int, str]] = None
    user_id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {'type': self.type}
        if self.chat_id:
            data['chat_id'] = self.chat_id
        if self.user_id:
            data['user_id'] = self.user_id
        return data
    
    @classmethod
    def default(cls) -> 'BotCommandScope':
        return cls(type='default')
    
    @classmethod
    def all_private_chats(cls) -> 'BotCommandScope':
        return cls(type='all_private_chats')
    
    @classmethod
    def all_group_chats(cls) -> 'BotCommandScope':
        return cls(type='all_group_chats')
    
    @classmethod
    def all_chat_administrators(cls) -> 'BotCommandScope':
        return cls(type='all_chat_administrators')
    
    @classmethod
    def all_private_chat_administrators(cls) -> 'BotCommandScope':
        return cls(type='all_private_chat_administrators')
    
    @classmethod
    def all_group_chat_administrators(cls) -> 'BotCommandScope':
        return cls(type='all_group_chat_administrators')
    
    @classmethod
    def chat(cls, chat_id: Union[int, str]) -> 'BotCommandScope':
        return cls(type='chat', chat_id=chat_id)
    
    @classmethod
    def chat_administrators(cls, chat_id: Union[int, str]) -> 'BotCommandScope':
        return cls(type='chat_administrators', chat_id=chat_id)
    
    @classmethod
    def chat_member(cls, chat_id: Union[int, str], user_id: int) -> 'BotCommandScope':
        return cls(type='chat_member', chat_id=chat_id, user_id=user_id)


# ==================== Payments ====================

@dataclass
class LabeledPrice:
    """Price portion of an invoice."""
    label: str
    amount: int  # Smallest currency unit (e.g., cents)
    
    def to_dict(self) -> Dict[str, Any]:
        return {'label': self.label, 'amount': self.amount}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LabeledPrice':
        return cls(
            label=data['label'],
            amount=data['amount']
        )


@dataclass
class ShippingOption:
    """One shipping option."""
    id: str
    title: str
    prices: List[LabeledPrice]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'prices': [p.to_dict() for p in self.prices]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ShippingOption':
        return cls(
            id=data['id'],
            title=data['title'],
            prices=[LabeledPrice.from_dict(p) for p in data['prices']]
        )


@dataclass
class StarTransaction:
    """Telegram Star transaction."""
    id: str
    amount: int
    date: int
    source: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StarTransaction':
        return cls(
            id=data['id'],
            amount=data['amount'],
            date=data['date'],
            source=data.get('source')
        )


@dataclass
class StarTransactions:
    """List of Star transactions."""
    transactions: List[StarTransaction]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StarTransactions':
        return cls(
            transactions=[StarTransaction.from_dict(t) for t in data.get('transactions', [])]
        )


# ==================== Games ====================

@dataclass
class Game:
    """A game."""
    title: str
    description: str
    photo: List[Any]  # List of PhotoSize
    text: Optional[str] = None
    text_entities: Optional[List[Any]] = None
    animation: Optional[Any] = None
    photo_list: Optional[List[Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Game':
        return cls(
            title=data['title'],
            description=data['description'],
            photo=data.get('photo', []),
            text=data.get('text'),
            text_entities=data.get('text_entities'),
            animation=data.get('animation'),
            photo_list=data.get('photo_list')
        )


@dataclass
class GameHighScore:
    """One row of game high scores."""
    position: int
    user: Any  # User object
    score: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameHighScore':
        return cls(
            position=data['position'],
            user=data['user'],
            score=data['score']
        )


# ==================== Forum/Topics ====================

@dataclass
class ForumTopic:
    """A forum topic."""
    message_thread_id: int
    name: str
    icon_color: Optional[int] = None
    icon_custom_emoji_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ForumTopic':
        return cls(
            message_thread_id=data['message_thread_id'],
            name=data['name'],
            icon_color=data.get('icon_color'),
            icon_custom_emoji_id=data.get('icon_custom_emoji_id')
        )


@dataclass
class ForumTopicCreated:
    """Service message about forum topic creation."""
    name: str
    icon_color: int
    icon_custom_emoji_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ForumTopicCreated':
        return cls(
            name=data['name'],
            icon_color=data['icon_color'],
            icon_custom_emoji_id=data.get('icon_custom_emoji_id')
        )


@dataclass
class ForumTopicClosed:
    """Service message about forum topic closure."""
    pass


@dataclass
class ForumTopicEdited:
    """Service message about forum topic edit."""
    name: Optional[str] = None
    icon_custom_emoji_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ForumTopicEdited':
        return cls(
            name=data.get('name'),
            icon_custom_emoji_id=data.get('icon_custom_emoji_id')
        )


@dataclass
class ForumTopicReopened:
    """Service message about forum topic reopen."""
    pass


@dataclass
class GeneralForumTopicHidden:
    """Service message about General forum topic hidden."""
    pass


@dataclass
class GeneralForumTopicUnhidden:
    """Service message about General forum topic unhidden."""
    pass


# ==================== Menu Button ====================

@dataclass
class MenuButton:
    """Describes the bot's menu button."""
    type: str  # commands, web_app, default
    text: Optional[str] = None
    web_app: Optional[Dict[str, str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {'type': self.type}
        if self.text:
            data['text'] = self.text
        if self.web_app:
            data['web_app'] = self.web_app
        return data
    
    @classmethod
    def commands(cls) -> 'MenuButton':
        return cls(type='commands')
    
    @classmethod
    def web_app(cls, text: str, url: str) -> 'MenuButton':
        return cls(type='web_app', text=text, web_app={'url': url})
    
    @classmethod
    def default(cls) -> 'MenuButton':
        return cls(type='default')


# ==================== Stickers ====================

@dataclass
class Sticker:
    """A sticker."""
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    type: str  # regular, mask, custom_emoji
    emoji: Optional[str] = None
    set_name: Optional[str] = None
    premium_animation: Optional[Any] = None
    mask_position: Optional[Any] = None
    custom_emoji_id: Optional[str] = None
    thumb: Optional[Any] = None
    file_size: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sticker':
        return cls(
            file_id=data['file_id'],
            file_unique_id=data['file_unique_id'],
            width=data['width'],
            height=data['height'],
            is_animated=data['is_animated'],
            is_video=data['is_video'],
            type=data.get('type', 'regular'),
            emoji=data.get('emoji'),
            set_name=data.get('set_name'),
            premium_animation=data.get('premium_animation'),
            mask_position=data.get('mask_position'),
            custom_emoji_id=data.get('custom_emoji_id'),
            thumb=data.get('thumb'),
            file_size=data.get('file_size')
        )


@dataclass
class StickerSet:
    """A sticker set."""
    name: str
    title: str
    sticker_type: str
    stickers: List[Sticker]
    is_animated: bool
    is_video: bool
    thumb: Optional[Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StickerSet':
        return cls(
            name=data['name'],
            title=data['title'],
            sticker_type=data.get('sticker_type', 'regular'),
            stickers=[Sticker.from_dict(s) for s in data.get('stickers', [])],
            is_animated=data.get('is_animated', False),
            is_video=data.get('is_video', False),
            thumb=data.get('thumb')
        )


@dataclass
class MaskPosition:
    """Position where a mask should be placed."""
    point: str  # forehead, eyes, chin
    x_shift: float
    y_shift: float
    scale: float
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MaskPosition':
        return cls(
            point=data['point'],
            x_shift=data['x_shift'],
            y_shift=data['y_shift'],
            scale=data['scale']
        )


# ==================== Reactions ====================

@dataclass
class ReactionType:
    """Type of reaction."""
    type: str  # emoji, custom_emoji
    emoji: Optional[str] = None
    custom_emoji_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = {'type': self.type}
        if self.emoji:
            data['emoji'] = self.emoji
        if self.custom_emoji_id:
            data['custom_emoji_id'] = self.custom_emoji_id
        return data
    
    @classmethod
    def emoji(cls, emoji: str) -> 'ReactionType':
        return cls(type='emoji', emoji=emoji)
    
    @classmethod
    def custom_emoji(cls, custom_emoji_id: str) -> 'ReactionType':
        return cls(type='custom_emoji', custom_emoji_id=custom_emoji_id)


@dataclass
class ReactionCount:
    """Reaction count of a specific type."""
    type: ReactionType
    total_count: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReactionCount':
        return cls(
            type=ReactionType(**data['type']),
            total_count=data['total_count']
        )


@dataclass
class MessageReactionUpdated:
    """Reaction changed on a message."""
    chat_id: int
    message_id: int
    user: Optional[Any] = None
    old_reaction: Optional[List[ReactionType]] = None
    new_reaction: Optional[List[ReactionType]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageReactionUpdated':
        return cls(
            chat_id=data['chat']['id'],
            message_id=data['message_id'],
            user=data.get('user'),
            old_reaction=[ReactionType(**r) for r in data.get('old_reaction', [])] if data.get('old_reaction') else None,
            new_reaction=[ReactionType(**r) for r in data.get('new_reaction', [])] if data.get('new_reaction') else None
        )


@dataclass
class MessageReactionCountUpdated:
    """Reactions changed on a message (channel posts)."""
    chat_id: int
    message_id: int
    reactions: List[ReactionCount]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MessageReactionCountUpdated':
        return cls(
            chat_id=data['chat']['id'],
            message_id=data['message_id'],
            reactions=[ReactionCount.from_dict(r) for r in data.get('reactions', [])]
        )


# ==================== Business ====================

@dataclass
class BusinessConnection:
    """Information about connection to a business account."""
    id: str
    user: Any  # User
    user_chat_id: int
    date: int
    can_reply: bool
    is_enabled: bool
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BusinessConnection':
        return cls(
            id=data['id'],
            user=data['user'],
            user_chat_id=data['user_chat_id'],
            date=data['date'],
            can_reply=data['can_reply'],
            is_enabled=data['is_enabled']
        )


@dataclass
class BusinessMessagesDeleted:
    """Messages deleted in a business chat."""
    business_connection_id: str
    chat_id: int
    message_ids: List[int]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BusinessMessagesDeleted':
        return cls(
            business_connection_id=data['business_connection_id'],
            chat_id=data['chat']['id'],
            message_ids=data['message_ids']
        )


@dataclass
class BusinessIntro:
    """Business intro info."""
    title: Optional[str] = None
    message: Optional[str] = None
    sticker: Optional[Sticker] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BusinessIntro':
        return cls(
            title=data.get('title'),
            message=data.get('message'),
            sticker=Sticker.from_dict(data['sticker']) if data.get('sticker') else None
        )


# ==================== Gifts ====================

@dataclass
class Gift:
    """A gift."""
    id: str
    sticker: Sticker
    star_count: int
    total_count: Optional[int] = None
    remaining_count: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Gift':
        return cls(
            id=data['id'],
            sticker=Sticker.from_dict(data['sticker']),
            star_count=data['star_count'],
            total_count=data.get('total_count'),
            remaining_count=data.get('remaining_count')
        )


@dataclass
class Gifts:
    """List of gifts."""
    gifts: List[Gift]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Gifts':
        return cls(
            gifts=[Gift.from_dict(g) for g in data.get('gifts', [])]
        )


# ==================== Verified Sections ====================

@dataclass
class ChatAvailableReactions:
    """Available reactions in a chat."""
    type: str  # all, some
    reactions: Optional[List[ReactionType]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatAvailableReactions':
        return cls(
            type=data['type'],
            reactions=[ReactionType(**r) for r in data.get('reactions', [])] if data.get('reactions') else None
        )


# ==================== API 9.6: Managed Bots ====================

@dataclass
class ManagedBotCreated:
    """Service message about a managed bot creation."""
    title: str
    username: str
    photo_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ManagedBotCreated':
        return cls(
            title=data.get('title', ''),
            username=data.get('username', ''),
            photo_url=data.get('photo_url')
        )


@dataclass
class ManagedBotUpdated:
    """Update about managed bot token change."""
    managed_bot_id: str
    new_token: Optional[str] = None
    date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ManagedBotUpdated':
        return cls(
            managed_bot_id=data.get('managed_bot_id', ''),
            new_token=data.get('new_token'),
            date=data.get('date')
        )


@dataclass
class ManagedBotInfo:
    """Information about a managed bot."""
    managed_bot_id: str
    title: str
    username: str
    is_active: bool = True
    created_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ManagedBotInfo':
        return cls(
            managed_bot_id=data.get('managed_bot_id', ''),
            title=data.get('title', ''),
            username=data.get('username', ''),
            is_active=data.get('is_active', True),
            created_date=data.get('created_date')
        )


@dataclass
class KeyboardButtonRequestManagedBot:
    """Represents a button to request a managed bot."""
    text: str
    bot_types: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {'text': self.text}
        if self.bot_types:
            data['bot_types'] = self.bot_types
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyboardButtonRequestManagedBot':
        return cls(
            text=data.get('text', ''),
            bot_types=data.get('bot_types')
        )


@dataclass
class PreparedKeyboardButton:
    """A prepared keyboard button for Mini Apps."""
    id: str
    text: str
    type: Optional[str] = None
    request_user: Optional[Dict] = None
    request_chat: Optional[Dict] = None
    request_managed_bot: Optional[KeyboardButtonRequestManagedBot] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {'id': self.id, 'text': self.text}
        if self.type:
            data['type'] = self.type
        if self.request_user:
            data['request_user'] = self.request_user
        if self.request_chat:
            data['request_chat'] = self.request_chat
        if self.request_managed_bot:
            data['request_managed_bot'] = self.request_managed_bot.to_dict()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PreparedKeyboardButton':
        return cls(
            id=data.get('id', ''),
            text=data.get('text', ''),
            type=data.get('type'),
            request_user=data.get('request_user'),
            request_chat=data.get('request_chat'),
            request_managed_bot=KeyboardButtonRequestManagedBot.from_dict(data['request_managed_bot']) if data.get('request_managed_bot') else None
        )


# ==================== API 9.6: Enhanced Polls ====================

@dataclass
class PollOptionExtended:
    """Extended poll option with new API 9.6 fields."""
    text: str
    voter_count: int
    # API 9.6 fields
    persistent_id: Optional[str] = None
    added_by_user: Optional[Any] = None  # User
    added_by_chat: Optional[Any] = None  # Chat
    addition_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PollOptionExtended':
        return cls(
            text=data.get('text', ''),
            voter_count=data.get('voter_count', 0),
            persistent_id=data.get('persistent_id'),
            added_by_user=data.get('added_by_user'),
            added_by_chat=data.get('added_by_chat'),
            addition_date=data.get('addition_date')
        )


@dataclass
class PollExtended:
    """Extended poll with API 9.6 features."""
    id: str
    question: str
    options: List[PollOptionExtended]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    poll_type: str  # regular, quiz
    allows_multiple_answers: bool = False
    # API 9.6 fields
    correct_option_ids: Optional[List[int]] = None
    allows_revoting: bool = False
    description: Optional[str] = None
    description_entities: Optional[List[Any]] = None
    shuffle_options: bool = False
    allow_adding_options: bool = False
    hide_results_until_closes: bool = False
    explanation: Optional[str] = None
    explanation_entities: Optional[List[Any]] = None
    open_period: Optional[int] = None
    close_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PollExtended':
        return cls(
            id=data.get('id', ''),
            question=data.get('question', ''),
            options=[PollOptionExtended.from_dict(opt) for opt in data.get('options', [])],
            total_voter_count=data.get('total_voter_count', 0),
            is_closed=data.get('is_closed', False),
            is_anonymous=data.get('is_anonymous', True),
            poll_type=data.get('type', 'regular'),
            allows_multiple_answers=data.get('allows_multiple_answers', False),
            correct_option_ids=data.get('correct_option_ids'),
            allows_revoting=data.get('allows_revoting', False),
            description=data.get('description'),
            description_entities=data.get('description_entities'),
            shuffle_options=data.get('shuffle_options', False),
            allow_adding_options=data.get('allow_adding_options', False),
            hide_results_until_closes=data.get('hide_results_until_closes', False),
            explanation=data.get('explanation'),
            explanation_entities=data.get('explanation_entities'),
            open_period=data.get('open_period'),
            close_date=data.get('close_date')
        )


@dataclass
class PollOptionAdded:
    """Service message about a new poll option added."""
    poll_id: str
    option_text: str
    option_persistent_id: Optional[str] = None
    added_by_user: Optional[Any] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PollOptionAdded':
        return cls(
            poll_id=data.get('poll_id', ''),
            option_text=data.get('option_text', ''),
            option_persistent_id=data.get('option_persistent_id'),
            added_by_user=data.get('added_by_user')
        )


@dataclass
class PollOptionDeleted:
    """Service message about a poll option deleted."""
    poll_id: str
    option_text: str
    option_persistent_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PollOptionDeleted':
        return cls(
            poll_id=data.get('poll_id', ''),
            option_text=data.get('option_text', ''),
            option_persistent_id=data.get('option_persistent_id')
        )


@dataclass
class PollAnswerExtended:
    """Extended poll answer with API 9.6 fields."""
    poll_id: str
    voter_chat: Optional[Any] = None
    user: Optional[Any] = None
    # API 9.6
    option_ids: Optional[List[int]] = None
    option_persistent_ids: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PollAnswerExtended':
        return cls(
            poll_id=data.get('poll_id', ''),
            voter_chat=data.get('voter_chat'),
            user=data.get('user'),
            option_ids=data.get('option_ids'),
            option_persistent_ids=data.get('option_persistent_ids')
        )


# ==================== API 9.6: Paid Media ====================

@dataclass
class PaidMedia:
    """Describes paid media."""
    type: str  # preview, photo, video

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaidMedia':
        return cls(type=data.get('type', 'preview'))


@dataclass
class PaidMediaPhoto(PaidMedia):
    """Paid media with photo."""
    photo: List[Any] = None  # List of PhotoSize

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaidMediaPhoto':
        return cls(
            type='photo',
            photo=data.get('photo', [])
        )


@dataclass
class PaidMediaVideo(PaidMedia):
    """Paid media with video."""
    video: Optional[Any] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaidMediaVideo':
        return cls(
            type='video',
            video=data.get('video'),
            width=data.get('width'),
            height=data.get('height'),
            duration=data.get('duration')
        )


@dataclass
class PaidMediaInfo:
    """Describes paid media purchased by user."""
    star_count: int
    paid_media: List[PaidMedia]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaidMediaInfo':
        return cls(
            star_count=data.get('star_count', 0),
            paid_media=[PaidMedia.from_dict(m) for m in data.get('paid_media', [])]
        )


# ==================== API 9.6: Invite Links ====================

@dataclass
class ChatInviteLink:
    """Represents an invite link for a chat."""
    invite_link: str
    creator: Any  # User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None
    reaction_type: Optional[ReactionType] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatInviteLink':
        return cls(
            invite_link=data.get('invite_link', ''),
            creator=data.get('creator'),
            creates_join_request=data.get('creates_join_request', False),
            is_primary=data.get('is_primary', False),
            is_revoked=data.get('is_revoked', False),
            name=data.get('name'),
            expire_date=data.get('expire_date'),
            member_limit=data.get('member_limit'),
            pending_join_request_count=data.get('pending_join_request_count'),
            reaction_type=ReactionType(**data['reaction_type']) if data.get('reaction_type') else None
        )


# ==================== API 9.6: Chat Permissions ====================

@dataclass
class ChatPermissions:
    """Describes default chat permissions."""
    can_send_messages: Optional[bool] = None
    can_send_audios: Optional[bool] = None
    can_send_documents: Optional[bool] = None
    can_send_photos: Optional[bool] = None
    can_send_videos: Optional[bool] = None
    can_send_video_notes: Optional[bool] = None
    can_send_voice_notes: Optional[bool] = None
    can_send_polls: Optional[bool] = None
    can_send_other_messages: Optional[bool] = None
    can_add_web_page_previews: Optional[bool] = None
    can_change_info: Optional[bool] = None
    can_invite_users: Optional[bool] = None
    can_pin_messages: Optional[bool] = None
    can_manage_topics: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if value is not None:
                data[field] = value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatPermissions':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @classmethod
    def all_allowed(cls) -> 'ChatPermissions':
        """Allow all permissions."""
        return cls(
            can_send_messages=True,
            can_send_audios=True,
            can_send_documents=True,
            can_send_photos=True,
            can_send_videos=True,
            can_send_video_notes=True,
            can_send_voice_notes=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_manage_topics=True
        )

    @classmethod
    def all_denied(cls) -> 'ChatPermissions':
        """Deny all permissions."""
        return cls(
            can_send_messages=False,
            can_send_audios=False,
            can_send_documents=False,
            can_send_photos=False,
            can_send_videos=False,
            can_send_video_notes=False,
            can_send_voice_notes=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_manage_topics=False
        )


# ==================== API 9.6: Administrator Rights ====================

@dataclass
class ChatAdministratorRights:
    """Rights of an administrator."""
    is_anonymous: bool = False
    can_manage_chat: bool = True
    can_delete_messages: bool = True
    can_manage_video_chats: bool = False
    can_restrict_members: bool = False
    can_promote_members: bool = False
    can_change_info: bool = False
    can_invite_users: bool = False
    can_post_stories: bool = False
    can_edit_stories: bool = False
    can_delete_stories: bool = False
    can_post_messages: bool = False
    can_edit_messages: bool = False
    can_pin_messages: bool = False
    can_manage_topics: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'is_anonymous': self.is_anonymous,
            'can_manage_chat': self.can_manage_chat,
            'can_delete_messages': self.can_delete_messages,
            'can_manage_video_chats': self.can_manage_video_chats,
            'can_restrict_members': self.can_restrict_members,
            'can_promote_members': self.can_promote_members,
            'can_change_info': self.can_change_info,
            'can_invite_users': self.can_invite_users,
            'can_post_stories': self.can_post_stories,
            'can_edit_stories': self.can_edit_stories,
            'can_delete_stories': self.can_delete_stories,
            'can_post_messages': self.can_post_messages,
            'can_edit_messages': self.can_edit_messages,
            'can_pin_messages': self.can_pin_messages,
            'can_manage_topics': self.can_manage_topics
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatAdministratorRights':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @classmethod
    def default(cls) -> 'ChatAdministratorRights':
        """Default administrator rights."""
        return cls()

    @classmethod
    def full(cls) -> 'ChatAdministratorRights':
        """Full administrator rights."""
        return cls(
            is_anonymous=True,
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_promote_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_post_stories=True,
            can_edit_stories=True,
            can_delete_stories=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_pin_messages=True,
            can_manage_topics=True
        )
