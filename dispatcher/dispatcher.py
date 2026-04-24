import asyncio
import logging
from typing import List, Callable, Dict, Optional, Any

from ..client import TelegramClient
from ..telegram_types import Update
from ..fsm import MemoryStorage, FSMContext
from .context import Context
from .middleware import MiddlewareManager
from .router import Router

logger = logging.getLogger(__name__)

class Dispatcher(Router):
    """
    Main dispatcher for handling updates, middleware, and FSM states.
    Inspired by the architecture of aiogram 3.x.
    
    Args:
        bot: Bot instance (optional, for convenience)
        storage: FSM storage instance (optional, defaults to MemoryStorage)
    """

    def __init__(self, bot: Optional[TelegramClient] = None, storage: Optional[Any] = None):
        super().__init__(name="dispatcher")
        self.bot = bot  # Store bot instance for convenience
        self.middleware_manager = MiddlewareManager()
        self._startup_hooks: List[Callable] = []
        self._shutdown_hooks: List[Callable] = []
        self._running = False

        # State storage (FSM) - defaults to MemoryStorage
        # Make sure we don't accidentally store the Bot object as storage
        if storage is not None and hasattr(storage, 'get_state'):
            # It's a valid storage object
            self.storage = storage
        else:
            # Use MemoryStorage by default
            self.storage = storage if hasattr(storage, 'get_state') else MemoryStorage()

    def middleware(self):
        """Decorator to register middleware"""
        def decorator(func: Callable):
            self.middleware_manager.add(func)
            return func
        return decorator

    def startup(self):
        """Decorator for startup hooks"""
        def decorator(func: Callable):
            self._startup_hooks.append(func)
            return func
        return decorator

    def shutdown(self):
        """Decorator for shutdown hooks"""
        def decorator(func: Callable):
            self._shutdown_hooks.append(func)
            return func
        return decorator

    async def process_update(self, client: TelegramClient, update_data: Dict):
        """Main method to process incoming updates from Telegram"""
        try:
            update = Update.from_dict(update_data)
            ctx = Context(client, update)

            # Inject FSMContext into the Context object
            if ctx.user_id:
                ctx.fsm = FSMContext(self.storage, ctx.user_id)
            else:
                ctx.fsm = None

            # Middleware chain runner
            async def run_handlers():
                # Router-based update feeding
                await self.feed_update(ctx)

            # Start the middleware chain
            await self.middleware_manager.run(ctx, run_handlers)

        except Exception as e:
            logger.error(f"Error while processing update: {e}", exc_info=True)

    async def start_polling(self, client: TelegramClient, skip_updates: bool = True):
        """Starts the bot in polling mode"""
        # Ensure webhook is deleted before starting polling
        try:
            await client.delete_webhook(drop_pending_updates=skip_updates)
        except Exception as e:
            logger.warning(f"Failed to delete webhook: {e}")

        print("🤖 Bot started! Press Ctrl+C to stop.")
        self._running = True
        offset = None

        # Execute startup hooks
        for hook in self._startup_hooks:
            await hook()

        try:
            if skip_updates:
                # Basic offset management to skip old updates
                updates = await client.get_updates(limit=1)
                if updates:
                    offset = updates[-1]['update_id'] + 1

            while self._running:
                try:
                    updates = await client.get_updates(offset=offset, timeout=30)
                    for update in updates:
                        offset = update['update_id'] + 1
                        # Asynchronous processing for each update
                        asyncio.create_task(self.process_update(client, update))

                    await asyncio.sleep(0.05)
                except Exception as e:
                    logger.error(f"Error in polling loop: {e}")
                    await asyncio.sleep(2)

        except KeyboardInterrupt:
            pass
        finally:
            self._running = False
            # Execute shutdown hooks
            for hook in self._shutdown_hooks:
                await hook()
            await client.close()
            print("\n✅ Bot has been safely shut down.")

    def run_polling(self, bot: TelegramClient, skip_updates: bool = True):
        """
        Synchronous wrapper to start polling (convenience method)
        
        Args:
            bot: Bot instance to use for polling
            skip_updates: Whether to skip pending updates on startup
        """
        import asyncio
        try:
            asyncio.run(self.start_polling(bot, skip_updates))
        except KeyboardInterrupt:
            print("\n✅ Bot stopped by user")
