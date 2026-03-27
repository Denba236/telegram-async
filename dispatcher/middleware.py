from typing import Callable, List, Any

from .context import Context


class MiddlewareManager:
    """Manages the execution of middleware in a chain-like fashion"""
    
    def __init__(self):
        self.middlewares: List[Callable] = []

    def add(self, middleware: Callable):
        """Adds a middleware function to the chain"""
        self.middlewares.append(middleware)

    async def run(self, ctx: Context, handler: Callable):
        """Executes the middleware chain"""

        index = 0

        async def next_middleware():
            nonlocal index
            if index < len(self.middlewares):
                current = self.middlewares[index]
                index += 1
                await current(ctx, next_middleware)
            else:
                await handler()

        await next_middleware()
