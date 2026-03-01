"""
Storage backends dla Finite State Machine (FSM)
"""
from typing import Optional, Any, Dict, Union, Callable, Type
import json
import logging

from .state import State, StatesGroup

logger = logging.getLogger(__name__)


class Storage:
    """Bazowa klasa dla storage'ów"""

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Ustawia stan dla użytkownika

        Args:
            user_id: ID użytkownika
            state: Stan do ustawienia (None = brak stanu)
        """
        raise NotImplementedError

    async def get_state(self, user_id: int) -> Optional[str]:
        """
        Pobiera stan użytkownika

        Args:
            user_id: ID użytkownika

        Returns:
            Aktualny stan jako string lub None
        """
        raise NotImplementedError

    async def set_data(self, user_id: int, data: Dict[str, Any]):
        """
        Ustawia dane dla użytkownika

        Args:
            user_id: ID użytkownika
            data: Dane do zapisania
        """
        raise NotImplementedError

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Pobiera dane użytkownika

        Args:
            user_id: ID użytkownika

        Returns:
            Słownik z danymi użytkownika
        """
        raise NotImplementedError

    async def update_data(self, user_id: int, **kwargs):
        """
        Aktualizuje dane użytkownika

        Args:
            user_id: ID użytkownika
            **kwargs: Pary klucz-wartość do aktualizacji
        """
        data = await self.get_data(user_id)
        data.update(kwargs)
        await self.set_data(user_id, data)

    async def clear(self, user_id: int):
        """
        Czyści stan i dane użytkownika

        Args:
            user_id: ID użytkownika
        """
        raise NotImplementedError

    async def close(self):
        """Zamyka połączenie ze storage'em"""
        pass


class MemoryStorage(Storage):
    """
    Storage w pamięci RAM

    Przykład:
        storage = MemoryStorage()
        await storage.set_state(123456, "state_name")
        state = await storage.get_state(123456)
    """

    def __init__(self):
        self.data: Dict[int, Dict[str, Any]] = {}
        self._state_resolvers: Dict[str, Callable] = {}

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Ustawia stan dla użytkownika w pamięci
        """
        if user_id not in self.data:
            self.data[user_id] = {"state": None, "data": {}}

        if isinstance(state, State):
            self.data[user_id]["state"] = str(state)
        else:
            self.data[user_id]["state"] = state

        logger.debug(f"MemoryStorage: set_state for user {user_id} -> {state}")

    async def get_state(self, user_id: int) -> Optional[str]:
        """
        Pobiera stan użytkownika z pamięci
        """
        state = self.data.get(user_id, {}).get("state")
        logger.debug(f"MemoryStorage: get_state for user {user_id} -> {state}")
        return state

    async def resolve_state(self, state_str: str) -> Optional[State]:
        """
        Konwertuje string na obiekt State jeśli możliwe

        Args:
            state_str: String reprezentujący stan

        Returns:
            Obiekt State lub None
        """
        # Sprawdź zarejestrowane resolvery
        for resolver in self._state_resolvers.values():
            state = resolver(state_str)
            if state:
                return state

        # Próbuj sparsować jako "Group:state"
        if ':' in state_str:
            group_name, state_name = state_str.split(':', 1)
            return State(state_name)

        return None

    def register_state_resolver(self, group: Type[StatesGroup]):
        """
        Rejestruje resolver dla grupy stanów

        Args:
            group: Klasa StatesGroup
        """

        def resolver(state_str: str) -> Optional[State]:
            for state in group._states.values():
                if str(state) == state_str:
                    return state
            return None

        self._state_resolvers[group.__name__] = resolver
        logger.debug(f"MemoryStorage: registered resolver for {group.__name__}")

    async def set_data(self, user_id: int, data: Dict[str, Any]):
        """
        Ustawia dane dla użytkownika w pamięci
        """
        if user_id not in self.data:
            self.data[user_id] = {"state": None, "data": {}}
        self.data[user_id]["data"] = data.copy()
        logger.debug(f"MemoryStorage: set_data for user {user_id} -> {len(data)} keys")

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Pobiera dane użytkownika z pamięci
        """
        data = self.data.get(user_id, {}).get("data", {}).copy()
        logger.debug(f"MemoryStorage: get_data for user {user_id} -> {len(data)} keys")
        return data

    async def update_data(self, user_id: int, **kwargs):
        """
        Aktualizuje dane użytkownika w pamięci
        """
        if user_id not in self.data:
            self.data[user_id] = {"state": None, "data": {}}
        self.data[user_id]["data"].update(kwargs)
        logger.debug(f"MemoryStorage: update_data for user {user_id} -> {kwargs}")

    async def clear(self, user_id: int):
        """
        Czyści stan i dane użytkownika z pamięci
        """
        if user_id in self.data:
            self.data[user_id] = {"state": None, "data": {}}
            logger.debug(f"MemoryStorage: cleared data for user {user_id}")

    async def clear_all(self):
        """Czyści wszystkie dane ze storage'u"""
        self.data.clear()
        logger.debug("MemoryStorage: cleared all data")

    def __contains__(self, user_id: int) -> bool:
        """Sprawdza czy użytkownik istnieje w storage"""
        return user_id in self.data

    def __len__(self) -> int:
        """Zwraca liczbę użytkowników w storage"""
        return len(self.data)


class RedisStorage(Storage):
    """
    Storage w Redis (wymaga redis-py)

    Przykład:
        import redis.asyncio as redis
        client = await redis.from_url("redis://localhost")
        storage = RedisStorage(client, prefix="my_bot")
        await storage.set_state(123456, "state_name")
        state = await storage.get_state(123456)
    """

    def __init__(self, redis_client, prefix: str = "fsm"):
        """
        Args:
            redis_client: Klient Redis (aioredis lub redis.asyncio)
            prefix: Prefiks dla kluczy w Redis
        """
        self.redis = redis_client
        self.prefix = prefix
        self._state_resolvers: Dict[str, Callable] = {}

    def _make_key(self, user_id: int, suffix: str) -> str:
        """
        Tworzy klucz Redis dla użytkownika

        Args:
            user_id: ID użytkownika
            suffix: Sufiks (np. "state" lub "data")

        Returns:
            Pełny klucz Redis
        """
        return f"{self.prefix}:{user_id}:{suffix}"

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Ustawia stan dla użytkownika w Redis
        """
        key = self._make_key(user_id, "state")

        if state is None:
            await self.redis.delete(key)
            logger.debug(f"RedisStorage: deleted state for user {user_id}")
        else:
            state_str = str(state) if isinstance(state, State) else state
            await self.redis.set(key, state_str)
            logger.debug(f"RedisStorage: set_state for user {user_id} -> {state_str}")

    async def get_state(self, user_id: int) -> Optional[str]:
        """
        Pobiera stan użytkownika z Redis
        """
        key = self._make_key(user_id, "state")
        state = await self.redis.get(key)

        if state:
            if isinstance(state, bytes):
                state = state.decode()
            logger.debug(f"RedisStorage: get_state for user {user_id} -> {state}")
            return state

        logger.debug(f"RedisStorage: get_state for user {user_id} -> None")
        return None

    async def resolve_state(self, state_str: str) -> Optional[State]:
        """
        Konwertuje string na obiekt State jeśli możliwe

        Args:
            state_str: String reprezentujący stan

        Returns:
            Obiekt State lub None
        """
        for resolver in self._state_resolvers.values():
            state = resolver(state_str)
            if state:
                return state
        return None

    def register_state_resolver(self, group: Type[StatesGroup]):
        """
        Rejestruje resolver dla grupy stanów

        Args:
            group: Klasa StatesGroup
        """

        def resolver(state_str: str) -> Optional[State]:
            for state in group._states.values():
                if str(state) == state_str:
                    return state
            return None

        self._state_resolvers[group.__name__] = resolver
        logger.debug(f"RedisStorage: registered resolver for {group.__name__}")

    async def set_data(self, user_id: int, data: Dict[str, Any]):
        """
        Ustawia dane dla użytkownika w Redis
        """
        key = self._make_key(user_id, "data")

        if data:
            await self.redis.set(key, json.dumps(data))
            logger.debug(f"RedisStorage: set_data for user {user_id} -> {len(data)} keys")
        else:
            await self.redis.delete(key)
            logger.debug(f"RedisStorage: deleted data for user {user_id}")

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Pobiera dane użytkownika z Redis
        """
        key = self._make_key(user_id, "data")
        data = await self.redis.get(key)

        if data:
            if isinstance(data, bytes):
                data = data.decode()
            result = json.loads(data)
            logger.debug(f"RedisStorage: get_data for user {user_id} -> {len(result)} keys")
            return result

        logger.debug(f"RedisStorage: get_data for user {user_id} -> empty dict")
        return {}

    async def update_data(self, user_id: int, **kwargs):
        """
        Aktualizuje dane użytkownika w Redis
        """
        data = await self.get_data(user_id)
        data.update(kwargs)
        await self.set_data(user_id, data)
        logger.debug(f"RedisStorage: update_data for user {user_id} -> {kwargs}")

    async def clear(self, user_id: int):
        """
        Czyści stan i dane użytkownika z Redis
        """
        state_key = self._make_key(user_id, "state")
        data_key = self._make_key(user_id, "data")

        await self.redis.delete(state_key, data_key)
        logger.debug(f"RedisStorage: cleared all data for user {user_id}")

    async def clear_all(self):
        """
        Czyści wszystkie dane wszystkich użytkowników z Redis
        Uwaga: Usuwa wszystkie klucze z podanym prefiksem!
        """
        pattern = f"{self.prefix}:*"
        keys = await self.redis.keys(pattern)

        if keys:
            await self.redis.delete(*keys)
            logger.debug(f"RedisStorage: cleared all data ({len(keys)} keys)")

    async def close(self):
        """Zamyka połączenie Redis"""
        await self.redis.close()
        logger.debug("RedisStorage: connection closed")


class MongoStorage(Storage):
    """
    Storage w MongoDB (wymaga motor)

    Przykład:
        import motor.motor_asyncio
        client = motor.motor_asyncio.AsyncIOMotorClient()
        db = client.my_database
        storage = MongoStorage(db, collection="fsm")
        await storage.set_state(123456, "state_name")
    """

    def __init__(self, database, collection: str = "fsm"):
        """
        Args:
            database: Instancja bazy danych MongoDB
            collection: Nazwa kolekcji
        """
        self.db = database
        self.collection = database[collection]
        self._state_resolvers: Dict[str, Callable] = {}

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Ustawia stan dla użytkownika w MongoDB
        """
        state_str = str(state) if isinstance(state, State) else state

        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"state": state_str}},
            upsert=True
        )
        logger.debug(f"MongoStorage: set_state for user {user_id} -> {state_str}")

    async def get_state(self, user_id: int) -> Optional[str]:
        """
        Pobiera stan użytkownika z MongoDB
        """
        doc = await self.collection.find_one({"_id": user_id})
        state = doc.get("state") if doc else None
        logger.debug(f"MongoStorage: get_state for user {user_id} -> {state}")
        return state

    async def resolve_state(self, state_str: str) -> Optional[State]:
        """
        Konwertuje string na obiekt State jeśli możliwe
        """
        for resolver in self._state_resolvers.values():
            state = resolver(state_str)
            if state:
                return state
        return None

    def register_state_resolver(self, group: Type[StatesGroup]):
        """
        Rejestruje resolver dla grupy stanów
        """

        def resolver(state_str: str) -> Optional[State]:
            for state in group._states.values():
                if str(state) == state_str:
                    return state
            return None

        self._state_resolvers[group.__name__] = resolver

    async def set_data(self, user_id: int, data: Dict[str, Any]):
        """
        Ustawia dane dla użytkownika w MongoDB
        """
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"data": data}},
            upsert=True
        )
        logger.debug(f"MongoStorage: set_data for user {user_id} -> {len(data)} keys")

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Pobiera dane użytkownika z MongoDB
        """
        doc = await self.collection.find_one({"_id": user_id})
        data = doc.get("data", {}) if doc else {}
        logger.debug(f"MongoStorage: get_data for user {user_id} -> {len(data)} keys")
        return data.copy()

    async def update_data(self, user_id: int, **kwargs):
        """
        Aktualizuje dane użytkownika w MongoDB
        """
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {f"data.{k}": v for k, v in kwargs.items()}},
            upsert=True
        )
        logger.debug(f"MongoStorage: update_data for user {user_id} -> {kwargs}")

    async def clear(self, user_id: int):
        """
        Czyści stan i dane użytkownika z MongoDB
        """
        await self.collection.delete_one({"_id": user_id})
        logger.debug(f"MongoStorage: cleared data for user {user_id}")

    async def clear_all(self):
        """Czyści wszystkie dane z MongoDB"""
        await self.collection.delete_many({})
        logger.debug("MongoStorage: cleared all data")


class InMemoryStorage(MemoryStorage):
    """
    Alias dla MemoryStorage dla zachowania kompatybilności
    """
    pass