"""
Throttling system (rate limiting) for telegram_async
"""
import time
import asyncio
import logging
from typing import Dict, Optional, Callable, Any, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ThrottleStrategy(Enum):
    """Throttling strategies"""
    WAIT = "wait"  # Wait for the limit to reset
    DROP = "drop"  # Drop the request
    QUEUE = "queue"  # Queue the requests


@dataclass
class ThrottleInfo:
    """Throttling information for a key"""
    timestamps: deque = field(default_factory=lambda: deque(maxlen=100))
    blocked_until: float = 0
    queue: deque = field(default_factory=deque)
    total_requests: int = 0
    dropped_requests: int = 0
    queued_requests: int = 0


class ThrottlingManager:
    """
    Advanced throttling manager

    Example:
        throttle = ThrottlingManager(rate=5, per=10)

        @dp.message()
        async def handler(ctx):
            if await throttle.check_user(ctx.user_id):
                await process_message(ctx)
            else:
                await ctx.answer("Too many requests!")
    """

    def __init__(
            self,
            default_rate: int = 5,
            default_per: int = 10,
            default_strategy: ThrottleStrategy = ThrottleStrategy.DROP,
            queue_size: int = 10
    ):
        """
        Args:
            default_rate: Default maximum number of requests
            default_per: Default period in seconds
            default_strategy: Default throttling strategy
            queue_size: Maximum queue size for QUEUE strategy
        """
        self.default_rate = default_rate
        self.default_per = default_per
        self.default_strategy = default_strategy
        self.queue_size = queue_size

        # Stores data for different key types
        self.users: Dict[int, ThrottleInfo] = defaultdict(ThrottleInfo)
        self.chats: Dict[int, ThrottleInfo] = defaultdict(ThrottleInfo)
        self.global_info = ThrottleInfo()

        # Custom keys
        self.custom: Dict[str, ThrottleInfo] = defaultdict(ThrottleInfo)

        # Configurations for specific keys
        self.configs: Dict[str, Dict] = {}

    def configure(
            self,
            key: str,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None
    ):
        """Configures throttling for a specific key"""
        self.configs[key] = {
            'rate': rate or self.default_rate,
            'per': per or self.default_per,
            'strategy': strategy or self.default_strategy
        }

    async def check(
            self,
            key: Union[str, int],
            key_type: str = "user",
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """
        Checks if the action can be performed

        Args:
            key: Key (e.g. user_id, chat_id)
            key_type: Key type ('user', 'chat', 'global', or custom name)
            rate: Maximum number of requests (override)
            per: Period in seconds (override)
            strategy: Throttling strategy (override)
            callback: Function called when the request is rejected

        Returns:
            True if the action can be performed
        """
        # Get configuration
        config_key = f"{key_type}:{key}" if key_type not in ['user', 'chat', 'global'] else key_type
        config = self.configs.get(config_key, {})

        rate = rate or config.get('rate') or self.default_rate
        per = per or config.get('per') or self.default_per
        strategy = strategy or config.get('strategy') or self.default_strategy

        # Get info for the key
        if key_type == "user":
            info = self.users[int(key)]
        elif key_type == "chat":
            info = self.chats[int(key)]
        elif key_type == "global":
            info = self.global_info
        else:
            info = self.custom[str(key)]

        info.total_requests += 1
        now = time.time()

        # Check block
        if info.blocked_until > now:
            info.dropped_requests += 1
            if callback:
                await callback(key, info.blocked_until - now)
            return False

        # Clear old timestamps
        while info.timestamps and now - info.timestamps[0] > per:
            info.timestamps.popleft()

        # Check limit
        if len(info.timestamps) < rate:
            info.timestamps.append(now)
            return True

        # Limit exceeded
        if strategy == ThrottleStrategy.WAIT:
            # Wait for the limit to release
            wait_time = info.timestamps[0] + per - now
            if wait_time > 0:
                logger.debug(f"Throttling: waiting {wait_time:.2f}s for {key_type}:{key}")
                await asyncio.sleep(wait_time)
                return await self.check(key, key_type, rate, per, strategy, callback)

        elif strategy == ThrottleStrategy.QUEUE:
            # Queue the request
            if len(info.queue) < self.queue_size:
                info.queued_requests += 1
                future = asyncio.Future()
                info.queue.append((now, future))

                # Process the queue
                if len(info.queue) == 1:
                    asyncio.create_task(self._process_queue(info, per))

                return await future
            else:
                info.dropped_requests += 1
                if callback:
                    await callback(key, per)
                return False

        # DROP - reject the request
        info.dropped_requests += 1
        if callback:
            await callback(key, per)
        return False

    async def _process_queue(self, info: ThrottleInfo, per: int):
        """Processes the request queue"""
        while info.queue:
            timestamp, future = info.queue[0]
            now = time.time()

            # Wait for the right moment
            wait_time = timestamp + per - now
            if wait_time > 0:
                await asyncio.sleep(wait_time)

            # Execute request
            info.timestamps.append(now)
            if not future.done():
                future.set_result(True)
            info.queue.popleft()

    async def check_user(
            self,
            user_id: int,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """Checks limit for a user"""
        return await self.check(user_id, "user", rate, per, strategy, callback)

    async def check_chat(
            self,
            chat_id: int,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """Checks limit for a chat"""
        return await self.check(chat_id, "chat", rate, per, strategy, callback)

    async def check_global(
            self,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """Checks global limit"""
        return await self.check("global", "global", rate, per, strategy, callback)

    def block_user(self, user_id: int, duration: float):
        """Blocks a user for a specified duration"""
        self.users[user_id].blocked_until = time.time() + duration
        logger.info(f"User {user_id} blocked for {duration}s")

    def unblock_user(self, user_id: int):
        """Unblocks a user"""
        self.users[user_id].blocked_until = 0
        logger.info(f"User {user_id} unblocked")

    def get_stats(self, key: Optional[Union[str, int]] = None, key_type: str = "user") -> Dict:
        """Returns statistics"""
        if key is not None:
            if key_type == "user":
                info = self.users.get(int(key))
            elif key_type == "chat":
                info = self.chats.get(int(key))
            elif key_type == "global":
                info = self.global_info
            else:
                info = self.custom.get(str(key))

            if info:
                return {
                    'total_requests': info.total_requests,
                    'dropped_requests': info.dropped_requests,
                    'queued_requests': info.queued_requests,
                    'queue_size': len(info.queue),
                    'blocked': info.blocked_until > time.time(),
                    'current_rate': len(info.timestamps)
                }
        else:
            # Aggregate statistics
            return {
                'total_users': len(self.users),
                'total_chats': len(self.chats),
                'global_requests': self.global_info.total_requests,
                'global_dropped': self.global_info.dropped_requests
            }
        return {}

    def reset_user(self, user_id: int):
        """Resets throttling for a user"""
        if user_id in self.users:
            del self.users[user_id]

    def reset_all(self):
        """Resets all throttling data"""
        self.users.clear()
        self.chats.clear()
        self.custom.clear()
        self.global_info = ThrottleInfo()


# Throttling decorator
def throttle(
        rate: Optional[int] = None,
        per: Optional[int] = None,
        key_func: Optional[Callable] = None,
        strategy: ThrottleStrategy = ThrottleStrategy.DROP,
        message: Optional[str] = None
):
    """
    Decorator for handler throttling

    Args:
        rate: Maximum number of calls
        per: Period in seconds
        key_func: Function returning the key for throttling
        strategy: Throttling strategy
        message: Message to send on rejection

    Example:
        @throttle(rate=3, per=1, message="Too fast!")
        @dp.message(Command("start"))
        async def start(ctx):
            await ctx.reply("Start")
    """
    manager = ThrottlingManager()

    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            # Get key
            if key_func:
                key = key_func(ctx)
            else:
                key = ctx.user_id or ctx.chat_id

            if not key:
                return await func(ctx, *args, **kwargs)

            # Rejection callback
            async def on_reject(key, wait_time):
                if message:
                    if '{wait}' in message:
                        msg = message.format(wait=int(wait_time))
                    else:
                        msg = message
                    await ctx.answer(msg)

            # Check throttling
            if await manager.check_user(
                    key,
                    rate=rate,
                    per=per,
                    strategy=strategy,
                    callback=on_reject if message else None
            ):
                return await func(ctx, *args, **kwargs)
            return None

        return wrapper

    return decorator


# Throttling middleware
class ThrottlingMiddleware:
    """Middleware for dispatcher throttling"""

    def __init__(
            self,
            manager: Optional[ThrottlingManager] = None,
            rate: int = 5,
            per: int = 10,
            message: str = "⏳ Too many requests. Please try again later."
    ):
        self.manager = manager or ThrottlingManager(rate, per)
        self.message = message
        self.logger = logging.getLogger(__name__)

    async def __call__(self, ctx, next_middleware):
        # Get user_id from context
        user_id = ctx.user_id

        if user_id:
            async def on_reject(key, wait_time):
                if self.message:
                    await ctx.answer(self.message)

            if await self.manager.check_user(user_id, callback=on_reject):
                return await next_middleware()
            else:
                self.logger.warning(f"Throttled user {user_id}")
                return None

        return await next_middleware()
