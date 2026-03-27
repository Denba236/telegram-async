from typing import Optional, Dict, Any, Union, List
import logging

from .storage import Storage
from .state import State

logger = logging.getLogger(__name__)


class FSMContext:
    """
    FSM Context for a specific user

    Example:
        @dp.message(Command("start"))
        async def start(ctx):
            await ctx.fsm.set_state(OrderStates.name)
            await ctx.fsm.update_data(user_id=ctx.user_id)
    """

    def __init__(self, storage: Storage, user_id: int):
        self.storage = storage
        self.user_id = user_id
        self._data: Optional[Dict] = None

    async def set_state(self, state: Optional[Union[str, State]]):
        """Sets the user's state"""
        await self.storage.set_state(self.user_id, state)
        logger.debug(f"User {self.user_id} state set to {state}")

    async def get_state(self) -> Optional[str]:
        """Gets the user's state as a string"""
        return await self.storage.get_state(self.user_id)

    async def get_state_obj(self) -> Optional[State]:
        """Gets the user's state as a State object"""
        state_str = await self.get_state()
        if not state_str:
            return None
        return await self.storage.resolve_state(state_str)

    async def set_data(self, data: Dict[str, Any]):
        """Sets user data"""
        await self.storage.set_data(self.user_id, data)
        self._data = data.copy()

    async def get_data(self) -> Dict[str, Any]:
        """Gets user data"""
        if self._data is None:
            self._data = await self.storage.get_data(self.user_id)
        return self._data.copy()

    async def update_data(self, **kwargs):
        """Updates user data"""
        await self.storage.update_data(self.user_id, **kwargs)
        if self._data is not None:
            self._data.update(kwargs)

    async def clear(self):
        """Clears the state and data for a user"""
        await self.storage.clear(self.user_id)
        self._data = None
        logger.debug(f"User {self.user_id} FSM cleared")

    async def set_callback_data(self, **kwargs):
        """Saves data for callback handlers"""
        await self.update_data(callback_data=kwargs)

    async def get_callback_data(self, key: Optional[str] = None):
        """Retrieves callback data"""
        data = await self.get_data()
        callback_data = data.get('callback_data', {})
        if key:
            return callback_data.get(key)
        return callback_data

    async def is_state(self, state: Union[str, State]) -> bool:
        """Checks if the user is in a given state"""
        current = await self.get_state()
        if not current:
            return False

        target = str(state) if isinstance(state, State) else state
        return current == target

    async def finish(self):
        """Finishes the FSM (alias for clear)"""
        await self.clear()


# FSM Decorators

def on_state(state: Union[str, State, List[Union[str, State]]]):
    """
    Decorator for handlers responding to a specific state

    Example:
        @on_state(OrderStates.name)
        async def process_name(ctx):
            name = ctx.message.text
            await ctx.fsm.update_data(name=name)
            await ctx.fsm.set_state(OrderStates.address)
    """
    from ..filters import state as state_filter
    return state_filter(state)


def on_enter_state(state: Union[str, State]):
    """Decorator for handlers called when entering a state"""

    def decorator(func):
        func.__fsm_on_enter__ = str(state)
        return func

    return decorator


def on_exit_state(state: Union[str, State]):
    """Decorator for handlers called when exiting a state"""

    def decorator(func):
        func.__fsm_on_exit__ = str(state)
        return func

    return decorator
