from typing import Optional, Dict, Any, Union,List
import logging

from .storage import Storage
from .state import State

logger = logging.getLogger(__name__)


class FSMContext:
    """
    Kontekst FSM dla konkretnego użytkownika

    Przykład:
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
        """Ustawia stan użytkownika"""
        await self.storage.set_state(self.user_id, state)
        logger.debug(f"User {self.user_id} state set to {state}")

    async def get_state(self) -> Optional[str]:
        """Pobiera stan użytkownika jako string"""
        return await self.storage.get_state(self.user_id)

    async def get_state_obj(self) -> Optional[State]:
        """Pobiera stan użytkownika jako obiekt State"""
        state_str = await self.get_state()
        if not state_str:
            return None
        return await self.storage.resolve_state(state_str)

    async def set_data(self, data: Dict[str, Any]):
        """Ustawia dane użytkownika"""
        await self.storage.set_data(self.user_id, data)
        self._data = data.copy()

    async def get_data(self) -> Dict[str, Any]:
        """Pobiera dane użytkownika"""
        if self._data is None:
            self._data = await self.storage.get_data(self.user_id)
        return self._data.copy()

    async def update_data(self, **kwargs):
        """Aktualizuje dane użytkownika"""
        await self.storage.update_data(self.user_id, **kwargs)
        if self._data is not None:
            self._data.update(kwargs)

    async def clear(self):
        """Czyści stan i dane użytkownika"""
        await self.storage.clear(self.user_id)
        self._data = None
        logger.debug(f"User {self.user_id} FSM cleared")

    async def set_callback_data(self, **kwargs):
        """Zapisuje dane dla callback handlerów"""
        await self.update_data(callback_data=kwargs)

    async def get_callback_data(self, key: Optional[str] = None):
        """Pobiera dane callback"""
        data = await self.get_data()
        callback_data = data.get('callback_data', {})
        if key:
            return callback_data.get(key)
        return callback_data

    async def is_state(self, state: Union[str, State]) -> bool:
        """Sprawdza czy użytkownik jest w danym stanie"""
        current = await self.get_state()
        if not current:
            return False

        target = str(state) if isinstance(state, State) else state
        return current == target

    async def finish(self):
        """Kończy FSM (alias dla clear)"""
        await self.clear()


# Dekoratory dla FSM

def on_state(state: Union[str, State, List[Union[str, State]]]):
    """
    Dekorator dla handlerów reagujących na konkretny stan

    Przykład:
        @on_state(OrderStates.name)
        async def process_name(ctx):
            name = ctx.message.text
            await ctx.fsm.update_data(name=name)
            await ctx.fsm.set_state(OrderStates.address)
    """
    from ..filters import state as state_filter
    return state_filter(state)


def on_enter_state(state: Union[str, State]):
    """Dekorator dla handlerów wywoływanych przy wejściu do stanu"""

    def decorator(func):
        func.__fsm_on_enter__ = str(state)
        return func

    return decorator


def on_exit_state(state: Union[str, State]):
    """Dekorator dla handlerów wywoływanych przy wyjściu ze stanu"""

    def decorator(func):
        func.__fsm_on_exit__ = str(state)
        return func

    return decorator