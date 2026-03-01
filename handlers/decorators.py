from functools import wraps


def role_required(role: str):
    """Dekorator wymagający odpowiedniej roli"""
    def decorator(func):
        func.__required_role__ = role
        return func
    return decorator


def command(name: str):
    """Dekorator dla komend"""
    def decorator(func):
        func.__command__ = name
        return func
    return decorator


def on_message(text_contains=None, from_user=None, chat_id=None):
    """Dekorator dla wiadomości"""
    def decorator(func):
        func.__on_message__ = True
        func.__filter__ = {
            "text_contains": text_contains,
            "from_user": from_user,
            "chat_id": chat_id
        }
        return func
    return decorator