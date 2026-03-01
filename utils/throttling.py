"""
System throttlingu (ograniczania częstotliwości) dla telegram_async
"""
import time
import asyncio
from typing import Dict, Optional, Callable, Any, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ThrottleStrategy(Enum):
    """Strategie throttlingu"""
    WAIT = "wait"  # Czekaj na zwolnienie limitu
    DROP = "drop"  # Odrzuć zapytanie
    QUEUE = "queue"  # Kolejkuj zapytania


@dataclass
class ThrottleInfo:
    """Informacje o throttlingu dla klucza"""
    timestamps: deque = field(default_factory=lambda: deque(maxlen=100))
    blocked_until: float = 0
    queue: deque = field(default_factory=deque)
    total_requests: int = 0
    dropped_requests: int = 0
    queued_requests: int = 0


class ThrottlingManager:
    """
    Zaawansowany menedżer throttlingu

    Przykład:
        throttle = ThrottlingManager(rate=5, per=10)

        @dp.message()
        async def handler(ctx):
            if await throttle.check_user(ctx.user_id):
                await process_message(ctx)
            else:
                await ctx.answer("Za dużo zapytań!")
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
            default_rate: Domyślna maksymalna liczba zapytań
            default_per: Domyślny okres w sekundach
            default_strategy: Domyślna strategia throttlingu
            queue_size: Maksymalny rozmiar kolejki dla strategii QUEUE
        """
        self.default_rate = default_rate
        self.default_per = default_per
        self.default_strategy = default_strategy
        self.queue_size = queue_size

        # Przechowuje dane dla różnych typów kluczy
        self.users: Dict[int, ThrottleInfo] = defaultdict(ThrottleInfo)
        self.chats: Dict[int, ThrottleInfo] = defaultdict(ThrottleInfo)
        self.global_info = ThrottleInfo()

        # Niestandardowe klucze
        self.custom: Dict[str, ThrottleInfo] = defaultdict(ThrottleInfo)

        # Konfiguracje dla konkretnych kluczy
        self.configs: Dict[str, Dict] = {}

    def configure(
            self,
            key: str,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None
    ):
        """Konfiguruje throttling dla konkretnego klucza"""
        self.configs[key] = {
            'rate': rate or self.default_rate,
            'per': per or self.default_per,
            'strategy': strategy or self.default_strategy
        }

    async def check(
            self,
            key: str,
            key_type: str = "user",
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """
        Sprawdza czy akcja może być wykonana

        Args:
            key: Klucz (np. user_id, chat_id)
            key_type: Typ klucza ('user', 'chat', 'global', lub nazwa własna)
            rate: Maksymalna liczba zapytań (override)
            per: Okres w sekundach (override)
            strategy: Strategia throttlingu (override)
            callback: Funkcja wywoływana przy odrzuceniu

        Returns:
            True jeśli akcja może być wykonana
        """
        # Pobierz konfigurację
        config_key = f"{key_type}:{key}" if key_type not in ['user', 'chat', 'global'] else key_type
        config = self.configs.get(config_key, {})

        rate = rate or config.get('rate') or self.default_rate
        per = per or config.get('per') or self.default_per
        strategy = strategy or config.get('strategy') or self.default_strategy

        # Pobierz info dla klucza
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

        # Sprawdź blokadę
        if info.blocked_until > now:
            info.dropped_requests += 1
            if callback:
                await callback(key, info.blocked_until - now)
            return False

        # Wyczyść stare timestampy
        while info.timestamps and now - info.timestamps[0] > per:
            info.timestamps.popleft()

        # Sprawdź limit
        if len(info.timestamps) < rate:
            info.timestamps.append(now)
            return True

        # Przekroczono limit
        if strategy == ThrottleStrategy.WAIT:
            # Czekaj na zwolnienie limitu
            wait_time = info.timestamps[0] + per - now
            if wait_time > 0:
                logger.debug(f"Throttling: waiting {wait_time:.2f}s for {key_type}:{key}")
                await asyncio.sleep(wait_time)
                return await self.check(key, key_type, rate, per, strategy, callback)

        elif strategy == ThrottleStrategy.QUEUE:
            # Kolejkuj zapytanie
            if len(info.queue) < self.queue_size:
                info.queued_requests += 1
                future = asyncio.Future()
                info.queue.append((now, future))

                # Przetwarzaj kolejkę
                if len(info.queue) == 1:
                    asyncio.create_task(self._process_queue(info, per))

                return await future
            else:
                info.dropped_requests += 1
                if callback:
                    await callback(key, per)
                return False

        # DROP - odrzuć zapytanie
        info.dropped_requests += 1
        if callback:
            await callback(key, per)
        return False

    async def _process_queue(self, info: ThrottleInfo, per: int):
        """Przetwarza kolejkę zapytań"""
        while info.queue:
            timestamp, future = info.queue[0]
            now = time.time()

            # Czekaj na odpowiedni moment
            wait_time = timestamp + per - now
            if wait_time > 0:
                await asyncio.sleep(wait_time)

            # Wykonaj zapytanie
            info.timestamps.append(now)
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
        """Sprawdza limit dla użytkownika"""
        return await self.check(user_id, "user", rate, per, strategy, callback)

    async def check_chat(
            self,
            chat_id: int,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """Sprawdza limit dla czatu"""
        return await self.check(chat_id, "chat", rate, per, strategy, callback)

    async def check_global(
            self,
            rate: Optional[int] = None,
            per: Optional[int] = None,
            strategy: Optional[ThrottleStrategy] = None,
            callback: Optional[Callable] = None
    ) -> bool:
        """Sprawdza globalny limit"""
        return await self.check("global", "global", rate, per, strategy, callback)

    def block_user(self, user_id: int, duration: float):
        """Blokuje użytkownika na określony czas"""
        self.users[user_id].blocked_until = time.time() + duration
        logger.info(f"User {user_id} blocked for {duration}s")

    def unblock_user(self, user_id: int):
        """Odblokowuje użytkownika"""
        self.users[user_id].blocked_until = 0
        logger.info(f"User {user_id} unblocked")

    def get_stats(self, key: Optional[str] = None, key_type: str = "user") -> Dict:
        """Zwraca statystyki"""
        if key and key_type:
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
            # Statystyki zbiorcze
            return {
                'total_users': len(self.users),
                'total_chats': len(self.chats),
                'global_requests': self.global_info.total_requests,
                'global_dropped': self.global_info.dropped_requests
            }
        return {}

    def reset_user(self, user_id: int):
        """Resetuje throttling dla użytkownika"""
        if user_id in self.users:
            del self.users[user_id]

    def reset_all(self):
        """Resetuje wszystkie throttlingi"""
        self.users.clear()
        self.chats.clear()
        self.custom.clear()
        self.global_info = ThrottleInfo()


# Dekorator do throttlingu
def throttle(
        rate: Optional[int] = None,
        per: Optional[int] = None,
        key_func: Optional[Callable] = None,
        strategy: ThrottleStrategy = ThrottleStrategy.DROP,
        message: Optional[str] = None
):
    """
    Dekorator do throttlingu handlerów

    Args:
        rate: Maksymalna liczba wywołań
        per: Okres w sekundach
        key_func: Funkcja zwracająca klucz do throttlingu
        strategy: Strategia throttlingu
        message: Wiadomość przy odrzuceniu

    Przykład:
        @throttle(rate=3, per=1, message="Za szybko!")
        @dp.message(Command("start"))
        async def start(ctx):
            await ctx.reply("Start")
    """
    manager = ThrottlingManager()

    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            # Pobierz klucz
            if key_func:
                key = key_func(ctx)
            else:
                key = ctx.user_id or ctx.chat_id

            if not key:
                return await func(ctx, *args, **kwargs)

            # Callback przy odrzuceniu
            async def on_reject(key, wait_time):
                if message:
                    if '{wait}' in message:
                        msg = message.format(wait=int(wait_time))
                    else:
                        msg = message
                    await ctx.answer(msg)

            # Sprawdź throttling
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


# Middleware throttlingu
class ThrottlingMiddleware:
    """Middleware do throttlingu dla dispatchera"""

    def __init__(
            self,
            manager: Optional[ThrottlingManager] = None,
            rate: int = 5,
            per: int = 10,
            message: str = "⏳ Zbyt wiele zapytań. Spróbuj później."
    ):
        self.manager = manager or ThrottlingManager(rate, per)
        self.message = message
        self.logger = logging.getLogger(__name__)

    async def __call__(self, ctx, next_middleware):
        # Pobierz user_id z kontekstu
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