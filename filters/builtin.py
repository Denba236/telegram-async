from typing import Optional, List, Union


def text(*texts: str):
    """
    Filter that checks if the message text is equal to one of the provided texts

    Example:
        @dp.message(text("yes", "no"))
        async def handle_yes_no(ctx):
            pass
    """

    async def filter_func(message):
        if not message.text:
            return False
        return message.text in texts

    return filter_func


def text_contains(*substrings: str):
    """
    Filter that checks if the message text contains one of the provided substrings

    Example:
        @dp.message(text_contains("hello", "hi"))
        async def handle_greeting(ctx):
            pass
    """

    async def filter_func(message):
        if not message.text:
            return False
        text_lower = message.text.lower()
        return any(sub.lower() in text_lower for sub in substrings)

    return filter_func


def chat_type(*types: str):
    """
    Filter that checks the chat type

    Types: 'private', 'group', 'supergroup', 'channel'

    Example:
        @dp.message(chat_type("private"))
        async def private_only(ctx):
            pass
    """

    async def filter_func(obj):
        chat = getattr(obj, 'chat', None)
        if not chat:
            return False
        return chat.type in types

    return filter_func


def from_user_id(*user_ids: int):
    """
    Filter that checks the user ID

    Example:
        @dp.message(from_user_id(123456, 789012))
        async def specific_users(ctx):
            pass
    """

    async def filter_func(obj):
        user = getattr(obj, 'from_user', None)
        if not user:
            return False
        return user.id in user_ids

    return filter_func


def chat_id(*chat_ids: int):
    """
    Filter that checks the chat ID

    Example:
        @dp.message(chat_id(-100123456))
        async def specific_chat(ctx):
            pass
    """

    async def filter_func(obj):
        chat = getattr(obj, 'chat', None)
        if not chat:
            return False
        return chat.id in chat_ids

    return filter_func


def reply_to_bot():
    """
    Filter that checks if the message is a reply to the bot
    """

    async def filter_func(message):
        if not message.reply_to_message:
            return False
        if not message.reply_to_message.from_user:
            return False
        return message.reply_to_message.from_user.is_bot

    return filter_func


def forward():
    """Filter that checks if the message is forwarded"""

    async def filter_func(message):
        return message.forward_from is not None or message.forward_from_chat is not None

    return filter_func
