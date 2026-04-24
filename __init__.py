"""
telegram_async - An asynchronous Telegram bot framework with workflow management.

Features:
    - Async Telegram Bot API client with retry logic
    - Dispatcher with decorator-based handlers
    - n8n-like workflow engine with visual nodes
    - FSM (Finite State Machine) support
    - Middleware system
    - Message filters
    - Inline & Reply keyboards
    - Built-in translation and text processing nodes
"""

# ============================================================================
# Version
# ============================================================================
from .version import __version__, __version_info__

# ============================================================================
# Core Client
# ============================================================================
from .client.bot import Bot
from .client.base import TelegramClient
from .client.webhook import WebhookServer
from .client.webhook_secret import SecretTokenValidation
from .client.methods import TelegramMethods

# ============================================================================
# Dispatcher
# ============================================================================
from .dispatcher.dispatcher import Dispatcher
from .dispatcher.context import Context
from .dispatcher.router import Router
from .dispatcher.middleware import MiddlewareManager as DispatcherMiddlewareManager

# ============================================================================
# Handlers & Decorators
# ============================================================================
from .handlers.decorators import command, on_message, role_required
from .handlers.callback import CallbackRegistry, callback_registry, on_callback

# ============================================================================
# FSM (Finite State Machine)
# ============================================================================
from .fsm.state import State, StatesGroup
from .fsm.storage import Storage, MemoryStorage, RedisStorage, MongoStorage, InMemoryStorage
from .fsm.context import FSMContext, on_state, on_enter_state, on_exit_state

# ============================================================================
# Filters
# ============================================================================
from .filters.base import (
    Filter,
    AndFilter,
    OrFilter,
    NotFilter,
    Command,
    Text,
    IsPrivate,
    IsGroup,
    IsChannel,
    IsReply,
    HasMedia,
    HasPhoto,
    HasDocument,
    FromUser,
    FromChat,
    CallbackData as CallbackDataFilter,
    CallbackMessage,
    State as StateFilter,
    AnyFilter,
    AllFilter,
    is_private,
    is_group,
    is_channel,
    is_reply,
    has_media,
    has_photo,
    has_document,
)
from .filters.command import Command as CommandFilter
from .filters.state import state as state_filter
from .filters.builtin import (
    text,
    text_contains,
    chat_type,
    from_user_id,
    chat_id,
    reply_to_bot,
    forward,
)

# ============================================================================
# Keyboards
# ============================================================================
from .keyboards.inline import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from .keyboards.reply import (
    ReplyKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from .keyboards.force_reply import ForceReply

# ============================================================================
# Middleware
# ============================================================================
from .middleware.base import (
    BaseMiddleware,
    MiddlewareManager,
    LoggingMiddleware,
    ThrottlingMiddleware,
    RoleMiddleware,
    FSMContextMiddleware,
    MetricsMiddleware,
    ErrorHandlingMiddleware,
    MiddlewareHandler,
    middleware,
)

# ============================================================================
# Exceptions
# ============================================================================
from .exceptions.exceptions import (
    TelegramError,
    TelegramAPIError,
    NetworkError,
    RateLimitError,
    ForbiddenError,
    NotFoundError,
    BadRequestError,
    ConflictError,
    UnauthorizedError,
    TimeoutError,
    SkipHandler,
    CancelHandler,
    ValidationError,
    WebhookError,
    FSMError,
    MiddlewareError,
    handle_telegram_error,
)

# ============================================================================
# Telegram Types
# ============================================================================
from .telegram_types import (
    # Base
    File,
    # User & Chat
    User, Chat, ChatPhoto, ChatPermissions, ChatLocation,
    # Message
    Message, MessageEntity, MessageAutoDeleteTimerChanged,
    # Media
    PhotoSize, Animation, Audio, Document, Video, VideoNote, Voice, Sticker, MaskPosition,
    # Inline
    InlineQuery, ChosenInlineResult, CallbackQuery,
    # Payments
    Invoice, SuccessfulPayment, OrderInfo, ShippingAddress, ShippingQuery, PreCheckoutQuery,
    # Passport
    PassportData, EncryptedPassportElement, PassportFile, EncryptedCredentials,
    # Misc
    Contact, Dice, Location, Venue, Poll, PollOption, Game,
    # Chat Member
    ChatMemberUpdated, ChatMember, ChatInviteLink, ChatJoinRequest,
    # Video Chat
    VideoChatScheduled, VideoChatStarted, VideoChatEnded, VideoChatParticipantsInvited,
    # Web App
    WebAppData,
    # Proximity
    ProximityAlertTriggered,
    # Poll Answer
    PollAnswer,
    # Update
    Update,
    # New API Types
    BotCommand, BotCommandScope, LabeledPrice, ShippingOption, StarTransaction, StarTransactions,
    GameHighScore, ForumTopic, ForumTopicCreated, ForumTopicClosed, ForumTopicEdited,
    ForumTopicReopened, GeneralForumTopicHidden, GeneralForumTopicUnhidden, MenuButton,
    StickerSet, ReactionType, ReactionCount, MessageReactionUpdated, MessageReactionCountUpdated,
    BusinessConnection, BusinessMessagesDeleted, BusinessIntro, Gift, Gifts, ChatAvailableReactions,
    ManagedBotCreated, ManagedBotUpdated, ManagedBotInfo, KeyboardButtonRequestManagedBot,
    PreparedKeyboardButton, PollOptionExtended, PollExtended, PollOptionAdded, PollOptionDeleted,
    PollAnswerExtended, PaidMedia, PaidMediaPhoto, PaidMediaVideo, PaidMediaInfo,
    ChatAdministratorRights, ReplyParameters,
)

# ============================================================================
# Utilities
# ============================================================================
from .utils.helpers import parse_command, split_text, escape_markdown, build_menu, extract_entities
from .utils.logger import logger, ColoredFormatter, setup_logger, get_logger, ContextLogger
from .utils.cache import TTLCache, RedisCache, FileCache, UpdateCache, cached
from .utils.throttling import (
    ThrottleStrategy,
    ThrottleInfo,
    ThrottlingManager,
    throttle,
    ThrottlingMiddleware as ThrottlingMiddlewareUtil,
)
from .utils.tasks import Scheduler
from .utils.i18n import I18n, I18nStorage, FileStorage as I18nFileStorage, gettext
from .utils.callback_factory import CallbackData, CompactCallbackData
from .utils.deep_linking import DeepLink
from .utils.background_tasks import BackgroundTask, BackgroundTasksManager
from .utils.metrics import MetricType, Metric, BotMetrics
from .utils.broadcast import BroadcastResult, BroadcastManager
from .utils.auto_delete import AutoDeleteManager
from .utils.testing import SentMessage, SentPhoto, MockBot, MockContext, run_handler_test

# ============================================================================
# Workflow Engine (n8n-like)
# ============================================================================
from .nodes import (
    WorkflowNode,
    NodeType,
    InputNode,
    DetectLanguageNode,
    TranslateNode,
    TransformNode,
    ConditionNode,
    OutputNode,
    NODE_TYPES,
)
from .manager import Workflow, WorkflowManager, workflow_manager
from .storage import WorkflowStorage, workflow_storage

# ============================================================================
# CLI
# ============================================================================
from .cli import CLI, main as cli_main

# ============================================================================
# Public API
# ============================================================================
__all__ = [
    # Version
    '__version__',
    '__version_info__',
    # Core Client
    'Bot',
    'TelegramClient',
    'WebhookServer',
    'SecretTokenValidation',
    'TelegramMethods',
    # Dispatcher
    'Dispatcher',
    'Context',
    'Router',
    'DispatcherMiddlewareManager',
    # Handlers
    'command',
    'on_message',
    'role_required',
    'CallbackRegistry',
    'callback_registry',
    'on_callback',
    # FSM
    'State',
    'StatesGroup',
    'Storage',
    'MemoryStorage',
    'RedisStorage',
    'MongoStorage',
    'InMemoryStorage',
    'FSMContext',
    'on_state',
    'on_enter_state',
    'on_exit_state',
    # Filters
    'Filter',
    'AndFilter',
    'OrFilter',
    'NotFilter',
    'Command',
    'CommandFilter',
    'Text',
    'IsPrivate',
    'IsGroup',
    'IsChannel',
    'IsReply',
    'HasMedia',
    'HasPhoto',
    'HasDocument',
    'FromUser',
    'FromChat',
    'CallbackDataFilter',
    'CallbackMessage',
    'StateFilter',
    'AnyFilter',
    'AllFilter',
    'is_private',
    'is_group',
    'is_channel',
    'is_reply',
    'has_media',
    'has_photo',
    'has_document',
    'state_filter',
    'text',
    'text_contains',
    'chat_type',
    'from_user_id',
    'chat_id',
    'reply_to_bot',
    'forward',
    # Keyboards
    'InlineKeyboardButton',
    'InlineKeyboardMarkup',
    'ReplyKeyboardButton',
    'ReplyKeyboardMarkup',
    'ReplyKeyboardRemove',
    'ForceReply',
    # Middleware
    'BaseMiddleware',
    'MiddlewareManager',
    'LoggingMiddleware',
    'ThrottlingMiddleware',
    'RoleMiddleware',
    'FSMContextMiddleware',
    'MetricsMiddleware',
    'ErrorHandlingMiddleware',
    'MiddlewareHandler',
    'middleware',
    # Exceptions
    'TelegramError',
    'TelegramAPIError',
    'NetworkError',
    'RateLimitError',
    'ForbiddenError',
    'NotFoundError',
    'BadRequestError',
    'ConflictError',
    'UnauthorizedError',
    'TimeoutError',
    'SkipHandler',
    'CancelHandler',
    'ValidationError',
    'WebhookError',
    'FSMError',
    'MiddlewareError',
    'handle_telegram_error',
    # Telegram Types - Base
    'File',
    'User',
    'Chat',
    'ChatPhoto',
    'ChatPermissions',
    'ChatLocation',
    # Telegram Types - Message
    'Message',
    'MessageEntity',
    'MessageAutoDeleteTimerChanged',
    # Telegram Types - Media
    'PhotoSize',
    'Animation',
    'Audio',
    'Document',
    'Video',
    'VideoNote',
    'Voice',
    'Sticker',
    'MaskPosition',
    # Telegram Types - Inline
    'InlineQuery',
    'ChosenInlineResult',
    'CallbackQuery',
    # Telegram Types - Payments
    'Invoice',
    'SuccessfulPayment',
    'OrderInfo',
    'ShippingAddress',
    'ShippingQuery',
    'PreCheckoutQuery',
    # Telegram Types - Passport
    'PassportData',
    'EncryptedPassportElement',
    'PassportFile',
    'EncryptedCredentials',
    # Telegram Types - Misc
    'Contact',
    'Dice',
    'Location',
    'Venue',
    'Poll',
    'PollOption',
    'Game',
    # Telegram Types - Chat Member
    'ChatMemberUpdated',
    'ChatMember',
    'ChatInviteLink',
    'ChatJoinRequest',
    # Telegram Types - Video Chat
    'VideoChatScheduled',
    'VideoChatStarted',
    'VideoChatEnded',
    'VideoChatParticipantsInvited',
    # Telegram Types - Web App
    'WebAppData',
    # Telegram Types - Proximity
    'ProximityAlertTriggered',
    # Telegram Types - Poll Answer
    'PollAnswer',
    # Telegram Types - Update
    'Update',
    # Telegram Types - New API Types
    'BotCommand',
    'BotCommandScope',
    'LabeledPrice',
    'ShippingOption',
    'StarTransaction',
    'StarTransactions',
    'GameHighScore',
    'ForumTopic',
    'ForumTopicCreated',
    'ForumTopicClosed',
    'ForumTopicEdited',
    'ForumTopicReopened',
    'GeneralForumTopicHidden',
    'GeneralForumTopicUnhidden',
    'MenuButton',
    'StickerSet',
    'ReactionType',
    'ReactionCount',
    'MessageReactionUpdated',
    'MessageReactionCountUpdated',
    'BusinessConnection',
    'BusinessMessagesDeleted',
    'BusinessIntro',
    'Gift',
    'Gifts',
    'ChatAvailableReactions',
    'ManagedBotCreated',
    'ManagedBotUpdated',
    'ManagedBotInfo',
    'KeyboardButtonRequestManagedBot',
    'PreparedKeyboardButton',
    'PollOptionExtended',
    'PollExtended',
    'PollOptionAdded',
    'PollOptionDeleted',
    'PollAnswerExtended',
    'PaidMedia',
    'PaidMediaPhoto',
    'PaidMediaVideo',
    'PaidMediaInfo',
    'ChatAdministratorRights',
    'ReplyParameters',
    # Utilities - Helpers
    'parse_command',
    'split_text',
    'escape_markdown',
    'build_menu',
    'extract_entities',
    # Utilities - Logger
    'logger',
    'ColoredFormatter',
    'setup_logger',
    'get_logger',
    'ContextLogger',
    # Utilities - Cache
    'TTLCache',
    'RedisCache',
    'FileCache',
    'UpdateCache',
    'cached',
    # Utilities - Throttling
    'ThrottleStrategy',
    'ThrottleInfo',
    'ThrottlingManager',
    'throttle',
    'ThrottlingMiddlewareUtil',
    # Utilities - Tasks
    'Scheduler',
    # Utilities - i18n
    'I18n',
    'I18nStorage',
    'I18nFileStorage',
    'gettext',
    # Utilities - Callback Factory
    'CallbackData',
    'CompactCallbackData',
    # Utilities - Deep Linking
    'DeepLink',
    # Utilities - Background Tasks
    'BackgroundTask',
    'BackgroundTasksManager',
    # Utilities - Metrics
    'MetricType',
    'Metric',
    'BotMetrics',
    # Utilities - Broadcast
    'BroadcastResult',
    'BroadcastManager',
    # Utilities - Auto Delete
    'AutoDeleteManager',
    # Utilities - Testing
    'SentMessage',
    'SentPhoto',
    'MockBot',
    'MockContext',
    'run_handler_test',
    # Workflow Engine
    'WorkflowNode',
    'NodeType',
    'InputNode',
    'DetectLanguageNode',
    'TranslateNode',
    'TransformNode',
    'ConditionNode',
    'OutputNode',
    'NODE_TYPES',
    'Workflow',
    'WorkflowManager',
    'workflow_manager',
    'WorkflowStorage',
    'workflow_storage',
    # CLI
    'CLI',
    'cli_main',
]
