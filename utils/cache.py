"""
System cachowania dla telegram_async
"""
import time
import asyncio
import pickle
import hashlib
import json
from typing import Any, Optional, Dict, List, Union, Callable
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TTLCache:
    """
    Cache z TTL (Time To Live) i ograniczeniem rozmiaru

    Przykład:
        cache = TTLCache(ttl=60, maxsize=100)
        cache.set("key", "value")
        value = cache.get("key")
    """

    def __init__(self, ttl: int = 60, maxsize: int = 1000):
        """
        Args:
            ttl: Czas życia wpisu w sekundach (None = bez TTL)
            maxsize: Maksymalny rozmiar cache
        """
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.expired = 0
        self.evicted = 0

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Pobiera wartość z cache

        Args:
            key: Klucz
            default: Wartość domyślna jeśli nie znaleziono

        Returns:
            Wartość z cache lub default
        """
        if key not in self.cache:
            self.misses += 1
            return default

        value, timestamp = self.cache[key]

        # Sprawdź TTL
        if self.ttl and time.time() - timestamp > self.ttl:
            del self.cache[key]
            self.expired += 1
            self.misses += 1
            return default

        # Przenieś na koniec (LRU)
        self.cache.move_to_end(key)
        self.hits += 1
        return value

    def set(self, key: Any, value: Any):
        """
        Zapisuje wartość w cache

        Args:
            key: Klucz
            value: Wartość
        """
        # Usuń najstarsze jeśli przekroczono limit
        if len(self.cache) >= self.maxsize:
            self.cache.popitem(last=False)
            self.evicted += 1

        self.cache[key] = (value, time.time())
        self.cache.move_to_end(key)

    def delete(self, key: Any):
        """Usuwa wpis z cache"""
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        """Czyści cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.expired = 0
        self.evicted = 0

    def get_all(self) -> Dict:
        """Zwraca wszystkie ważne wpisy"""
        now = time.time()
        result = {}
        expired_keys = []

        for key, (value, timestamp) in self.cache.items():
            if self.ttl and now - timestamp > self.ttl:
                expired_keys.append(key)
            else:
                result[key] = value

        # Usuń przeterminowane
        for key in expired_keys:
            del self.cache[key]
            self.expired += 1

        return result

    def get_stats(self) -> Dict:
        """Zwraca statystyki cache"""
        total = self.hits + self.misses
        return {
            'size': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': (self.hits / total * 100) if total > 0 else 0,
            'expired': self.expired,
            'evicted': self.evicted,
            'maxsize': self.maxsize,
            'ttl': self.ttl
        }

    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None

    def __len__(self) -> int:
        return len(self.cache)

    def __repr__(self) -> str:
        return f"<TTLCache size={len(self.cache)} hits={self.hits} misses={self.misses}>"


class RedisCache:
    """
    Cache w Redis (wymaga redis-py)

    Przykład:
        import redis.asyncio as redis
        client = await redis.from_url("redis://localhost")
        cache = RedisCache(client, ttl=60)
        await cache.set("key", "value")
        value = await cache.get("key")
    """

    def __init__(
            self,
            redis_client,
            ttl: int = 60,
            prefix: str = "cache",
            serializer: Optional[Callable] = None,
            deserializer: Optional[Callable] = None
    ):
        """
        Args:
            redis_client: Klient Redis (aioredis lub redis.asyncio)
            ttl: Domyślny TTL w sekundach
            prefix: Prefiks dla kluczy
            serializer: Funkcja serializująca (domyślnie pickle)
            deserializer: Funkcja deserializująca (domyślnie pickle)
        """
        self.redis = redis_client
        self.ttl = ttl
        self.prefix = prefix
        self.serializer = serializer or pickle.dumps
        self.deserializer = deserializer or pickle.loads
        self.hits = 0
        self.misses = 0

    def _make_key(self, key: Any) -> str:
        """Tworzy klucz Redis z prefiksem"""
        if isinstance(key, (str, int, float)):
            key_str = str(key)
        else:
            # Hash dla złożonych kluczy
            key_str = hashlib.md5(str(key).encode()).hexdigest()
        return f"{self.prefix}:{key_str}"

    async def get(self, key: Any, default: Any = None) -> Any:
        """
        Pobiera wartość z cache
        """
        redis_key = self._make_key(key)
        data = await self.redis.get(redis_key)

        if data is None:
            self.misses += 1
            return default

        try:
            value = self.deserializer(data)
            self.hits += 1
            return value
        except Exception as e:
            logger.error(f"Failed to deserialize cache key {key}: {e}")
            await self.redis.delete(redis_key)
            self.misses += 1
            return default

    async def set(self, key: Any, value: Any, ttl: Optional[int] = None):
        """
        Zapisuje wartość w cache
        """
        redis_key = self._make_key(key)
        ttl = ttl or self.ttl

        try:
            data = self.serializer(value)
            if ttl:
                await self.redis.setex(redis_key, ttl, data)
            else:
                await self.redis.set(redis_key, data)
        except Exception as e:
            logger.error(f"Failed to serialize cache key {key}: {e}")

    async def delete(self, key: Any):
        """Usuwa wpis z cache"""
        redis_key = self._make_key(key)
        await self.redis.delete(redis_key)

    async def clear(self):
        """Czyści wszystkie wpisy z prefiksem"""
        pattern = f"{self.prefix}:*"
        keys = await self.redis.keys(pattern)
        if keys:
            await self.redis.delete(*keys)
        self.hits = 0
        self.misses = 0

    async def get_stats(self) -> Dict:
        """Zwraca statystyki"""
        pattern = f"{self.prefix}:*"
        keys = await self.redis.keys(pattern)
        total = self.hits + self.misses
        return {
            'size': len(keys),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': (self.hits / total * 100) if total > 0 else 0,
            'ttl': self.ttl
        }

    async def close(self):
        """Zamyka połączenie Redis"""
        await self.redis.close()


class UpdateCache:
    """
    Specjalizowany cache dla aktualizacji Telegram

    Przykład:
        update_cache = UpdateCache(ttl=60)
        if not update_cache.is_processed(update_id):
            await process_update(update)
            update_cache.add(update_id)
    """

    def __init__(self, ttl: int = 60, maxsize: int = 10000):
        """
        Args:
            ttl: Czas przechowywania update_id w sekundach
            maxsize: Maksymalna liczba przechowywanych ID
        """
        self.cache = TTLCache(ttl=ttl, maxsize=maxsize)

    def add(self, update_id: int):
        """Dodaje update_id do cache"""
        self.cache.set(update_id, time.time())

    def is_processed(self, update_id: int) -> bool:
        """Sprawdza czy update został już przetworzony"""
        return update_id in self.cache

    def remove(self, update_id: int):
        """Usuwa update_id z cache"""
        self.cache.delete(update_id)

    def clear(self):
        """Czyści cache"""
        self.cache.clear()

    def get_stats(self) -> Dict:
        """Zwraca statystyki cache"""
        return self.cache.get_stats()


class FileCache:
    """
    Cache plikowy (dla dużych danych)

    Przykład:
        cache = FileCache(cache_dir="./cache")
        await cache.set("key", large_data)
        data = await cache.get("key")
    """

    def __init__(self, cache_dir: str = "./cache", ttl: int = 3600):
        """
        Args:
            cache_dir: Katalog na pliki cache
            ttl: Domyślny TTL w sekundach
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        self._ensure_cache_dir()
        self.memory_cache = TTLCache(ttl=60, maxsize=100)  # Mały cache w pamięci

    def _ensure_cache_dir(self):
        """Tworzy katalog cache jeśli nie istnieje"""
        import os
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_path(self, key: Any) -> str:
        """Zwraca ścieżkę do pliku cache"""
        import os
        if isinstance(key, (str, int, float)):
            key_str = str(key).replace('/', '_').replace('\\', '_')
        else:
            key_str = hashlib.md5(str(key).encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_str}.cache")

    async def get(self, key: Any, default: Any = None) -> Any:
        """
        Pobiera wartość z cache plikowego
        """
        import os
        import aiofiles
        import pickle

        # Sprawdź cache w pamięci
        mem_value = self.memory_cache.get(key)
        if mem_value is not None:
            return mem_value

        path = self._get_path(key)

        try:
            if not os.path.exists(path):
                return default

            # Sprawdź TTL
            mtime = os.path.getmtime(path)
            if self.ttl and time.time() - mtime > self.ttl:
                os.unlink(path)
                return default

            async with aiofiles.open(path, 'rb') as f:
                data = await f.read()
                value = pickle.loads(data)

                # Zapisz w cache pamięci
                self.memory_cache.set(key, value)
                return value

        except Exception as e:
            logger.error(f"Failed to read cache file {path}: {e}")
            return default

    async def set(self, key: Any, value: Any, ttl: Optional[int] = None):
        """
        Zapisuje wartość do cache plikowego
        """
        import aiofiles
        import pickle

        path = self._get_path(key)

        try:
            data = pickle.dumps(value)
            async with aiofiles.open(path, 'wb') as f:
                await f.write(data)

            # Zapisz w cache pamięci
            self.memory_cache.set(key, value)

        except Exception as e:
            logger.error(f"Failed to write cache file {path}: {e}")

    async def delete(self, key: Any):
        """Usuwa wpis z cache"""
        import os
        path = self._get_path(key)
        self.memory_cache.delete(key)

        try:
            if os.path.exists(path):
                os.unlink(path)
        except Exception as e:
            logger.error(f"Failed to delete cache file {path}: {e}")

    async def clear(self):
        """Czyści cały cache plikowy"""
        import os
        import glob

        self.memory_cache.clear()

        try:
            pattern = os.path.join(self.cache_dir, "*.cache")
            for path in glob.glob(pattern):
                os.unlink(path)
        except Exception as e:
            logger.error(f"Failed to clear cache directory: {e}")

    async def get_stats(self) -> Dict:
        """Zwraca statystyki cache"""
        import os
        import glob

        pattern = os.path.join(self.cache_dir, "*.cache")
        files = glob.glob(pattern)

        total_size = 0
        for f in files:
            total_size += os.path.getsize(f)

        return {
            'size': len(files),
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'memory_cache': self.memory_cache.get_stats()
        }


# Dekorator do cachowania wyników funkcji
def cached(cache: Union[TTLCache, RedisCache, FileCache], key_func: Optional[Callable] = None):
    """
    Dekorator cachujący wyniki funkcji

    Args:
        cache: Instancja cache
        key_func: Funkcja generująca klucz cache

    Przykład:
        cache = TTLCache(ttl=60)

        @cached(cache)
        async def get_user_info(user_id):
            return await api.get_user(user_id)
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generuj klucz cache
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Domyślny klucz z argumentów
                cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Próba pobrania z cache
            result = await cache.get(cache_key)
            if result is not None:
                return result

            # Wykonaj funkcję
            result = await func(*args, **kwargs)

            # Zapisz w cache
            await cache.set(cache_key, result)

            return result

        return wrapper

    return decorator