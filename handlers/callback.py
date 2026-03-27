from collections import defaultdict


class CallbackRegistry:
    def __init__(self):
        # pattern -> handler
        self.handlers = {}

    def register(self, pattern: str, handler):
        self.handlers[pattern] = handler

    async def dispatch(self, ctx, callback_data: str):
        for pattern, handler in self.handlers.items():
            if pattern == callback_data:
                await handler(ctx)
                return


# Singleton for framework use
callback_registry = CallbackRegistry()


def on_callback(pattern: str):
    """Decorator for callback query"""
    def wrapper(func):
        callback_registry.register(pattern, func)
        return func
    return wrapper
