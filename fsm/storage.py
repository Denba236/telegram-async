"""
Storage backends for Finite State Machine (FSM)
"""
from typing import Optional, Any, Dict, Union, Callable, Type
import json
import logging

from .state import State, StatesGroup

logger = logging.getLogger(__name__)


class Storage:
    """Base class for storage backends"""

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Sets the state for a user

        Args:
            user_id: User ID
            state: State to set (None = no state)
        """
        raise NotImplementedError

    async def get_state(self, user_id: int) -> Optional[str]:
        """
        Gets the user's state

        Args:
            user_id: User ID

        Returns:
            Current state as a string or None
        """
        raise NotImplementedError

    async def set_data(self, user_id: int, data: Dict[str, Any]):
        """
        Sets data for a user

        Args:
            user_id: User ID
            data: Data to save
        """
        raise NotImplementedError

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Gets user data

        Args:
            user_id: User ID

        Returns:
            Dictionary with user data
        """
        raise NotImplementedError

    async def update_data(self, user_id: int, **kwargs):
        """
        Updates user data

        Args:
            user_id: User ID
            **kwargs: Key-value pairs to update
        """
        data = await self.get_data(user_id)
        data.update(kwargs)
        await self.set_data(user_id, data)

    async def clear(self, user_id: int):
        """
        Clears the state and data for a user

        Args:
            user_id: User ID
        """
        raise NotImplementedError

    async def close(self):
        """Closes the connection to the storage"""
        pass


class MemoryStorage(Storage):
    """
    In-memory RAM storage

    Example:
        storage = MemoryStorage()
        await storage.set_state(123456, "state_name")
        state = await storage.get_state(123456)
    """

    def __init__(self):
        self.data: Dict[int, Dict[str, Any]] = {}
        self._state_resolvers: Dict[str, Callable] = {}

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Sets the state for a user in memory
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
        Gets the user's state from memory
        """
        state = self.data.get(user_id, {}).get("state")
        logger.debug(f"MemoryStorage: get_state for user {user_id} -> {state}")
        return state

    async def resolve_state(self, state_str: str) -> Optional[State]:
        """
        Converts a string to a State object if possible

        Args:
            state_str: String representing the state

        Returns:
            State object or None
        """
        # Check registered resolvers
        for resolver in self._state_resolvers.values():
            state = resolver(state_str)
            if state:
                return state

        # Try to parse as "Group:state"
        if ':' in state_str:
            group_name, state_name = state_str.split(':', 1)
            return State(state_name)

        return None

    def register_state_resolver(self, group: Type[StatesGroup]):
        """
        Registers a resolver for a group of states

        Args:
            group: StatesGroup class
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
        Sets data for a user in memory
        """
        if user_id not in self.data:
            self.data[user_id] = {"state": None, "data": {}}
        self.data[user_id]["data"] = data.copy()
        logger.debug(f"MemoryStorage: set_data for user {user_id} -> {len(data)} keys")

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Gets user data from memory
        """
        data = self.data.get(user_id, {}).get("data", {}).copy()
        logger.debug(f"MemoryStorage: get_data for user {user_id} -> {len(data)} keys")
        return data

    async def update_data(self, user_id: int, **kwargs):
        """
        Updates user data in memory
        """
        if user_id not in self.data:
            self.data[user_id] = {"state": None, "data": {}}
        self.data[user_id]["data"].update(kwargs)
        logger.debug(f"MemoryStorage: update_data for user {user_id} -> {kwargs}")

    async def clear(self, user_id: int):
        """
        Clears the state and data for a user in memory
        """
        if user_id in self.data:
            self.data[user_id] = {"state": None, "data": {}}
            logger.debug(f"MemoryStorage: cleared data for user {user_id}")

    async def clear_all(self):
        """Clears all data from storage"""
        self.data.clear()
        logger.debug("MemoryStorage: cleared all data")

    def __contains__(self, user_id: int) -> bool:
        """Checks if a user exists in storage"""
        return user_id in self.data

    def __len__(self) -> int:
        """Returns the number of users in storage"""
        return len(self.data)


class RedisStorage(Storage):
    """
    Redis storage (requires redis-py)

    Example:
        import redis.asyncio as redis
        client = await redis.from_url("redis://localhost")
        storage = RedisStorage(client, prefix="my_bot")
        await storage.set_state(123456, "state_name")
        state = await storage.get_state(123456)
    """

    def __init__(self, redis_client, prefix: str = "fsm"):
        """
        Args:
            redis_client: Redis client (aioredis or redis.asyncio)
            prefix: Prefix for keys in Redis
        """
        self.redis = redis_client
        self.prefix = prefix
        self._state_resolvers: Dict[str, Callable] = {}

    def _make_key(self, user_id: int, suffix: str) -> str:
        """
        Creates a Redis key for a user

        Args:
            user_id: User ID
            suffix: Suffix (e.g. "state" or "data")

        Returns:
            Full Redis key
        """
        return f"{self.prefix}:{user_id}:{suffix}"

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Sets the state for a user in Redis
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
        Gets the user's state from Redis
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
        Converts a string to a State object if possible

        Args:
            state_str: String representing the state

        Returns:
            State object or None
        """
        for resolver in self._state_resolvers.values():
            state = resolver(state_str)
            if state:
                return state
        return None

    def register_state_resolver(self, group: Type[StatesGroup]):
        """
        Registers a resolver for a group of states

        Args:
            group: StatesGroup class
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
        Sets data for a user in Redis
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
        Gets user data from Redis
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
        Updates user data in Redis
        """
        data = await self.get_data(user_id)
        data.update(kwargs)
        await self.set_data(user_id, data)
        logger.debug(f"RedisStorage: update_data for user {user_id} -> {kwargs}")

    async def clear(self, user_id: int):
        """
        Clears the state and data for a user in Redis
        """
        state_key = self._make_key(user_id, "state")
        data_key = self._make_key(user_id, "data")

        await self.redis.delete(state_key, data_key)
        logger.debug(f"RedisStorage: cleared all data for user {user_id}")

    async def clear_all(self):
        """
        Clears all data for all users from Redis
        Note: Deletes all keys with the specified prefix!
        """
        pattern = f"{self.prefix}:*"
        keys = await self.redis.keys(pattern)

        if keys:
            await self.redis.delete(*keys)
            logger.debug(f"RedisStorage: cleared all data ({len(keys)} keys)")

    async def close(self):
        """Closes the Redis connection"""
        await self.redis.close()
        logger.debug("RedisStorage: connection closed")


class MongoStorage(Storage):
    """
    MongoDB storage (requires motor)

    Example:
        import motor.motor_asyncio
        client = motor.motor_asyncio.AsyncIOMotorClient()
        db = client.my_database
        storage = MongoStorage(db, collection="fsm")
        await storage.set_state(123456, "state_name")
    """

    def __init__(self, database, collection: str = "fsm"):
        """
        Args:
            database: MongoDB database instance
            collection: Collection name
        """
        self.db = database
        self.collection = database[collection]
        self._state_resolvers: Dict[str, Callable] = {}

    async def set_state(self, user_id: int, state: Optional[Union[str, State]]):
        """
        Sets the state for a user in MongoDB
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
        Gets the user's state from MongoDB
        """
        doc = await self.collection.find_one({"_id": user_id})
        state = doc.get("state") if doc else None
        logger.debug(f"MongoStorage: get_state for user {user_id} -> {state}")
        return state

    async def resolve_state(self, state_str: str) -> Optional[State]:
        """
        Converts a string to a State object if possible
        """
        for resolver in self._state_resolvers.values():
            state = resolver(state_str)
            if state:
                return state
        return None

    def register_state_resolver(self, group: Type[StatesGroup]):
        """
        Registers a resolver for a group of states
        """

        def resolver(state_str: str) -> Optional[State]:
            for state in group._states.values():
                if str(state) == state_str:
                    return state
            return None

        self._state_resolvers[group.__name__] = resolver

    async def set_data(self, user_id: int, data: Dict[str, Any]):
        """
        Sets data for a user in MongoDB
        """
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"data": data}},
            upsert=True
        )
        logger.debug(f"MongoStorage: set_data for user {user_id} -> {len(data)} keys")

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        """
        Gets user data from MongoDB
        """
        doc = await self.collection.find_one({"_id": user_id})
        data = doc.get("data", {}) if doc else {}
        logger.debug(f"MongoStorage: get_data for user {user_id} -> {len(data)} keys")
        return data.copy()

    async def update_data(self, user_id: int, **kwargs):
        """
        Updates user data in MongoDB
        """
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {f"data.{k}": v for k, v in kwargs.items()}},
            upsert=True
        )
        logger.debug(f"MongoStorage: update_data for user {user_id} -> {kwargs}")

    async def clear(self, user_id: int):
        """
        Clears the state and data for a user in MongoDB
        """
        await self.collection.delete_one({"_id": user_id})
        logger.debug(f"MongoStorage: cleared data for user {user_id}")

    async def clear_all(self):
        """Clears all data from MongoDB"""
        await self.collection.delete_many({})
        logger.debug("MongoStorage: cleared all data")


class InMemoryStorage(MemoryStorage):
    """
    Alias for MemoryStorage for backward compatibility
    """
    pass
