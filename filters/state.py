from typing import Optional, Union, List

from ..fsm import State


def state(state_value: Optional[Union[str, State, List[Union[str, State]]]]):
    """
    Filtr sprawdzający stan użytkownika

    Przykład:
        @dp.message(state(OrderStates.waiting_for_name))
        async def process_name(ctx):
            pass

        @dp.message(state(None))  # Tylko gdy brak stanu
        async def no_state(ctx):
            pass
    """

    async def filter_func(obj):
        # Logika w dispatcherze
        return True

    filter_func._state_filter = state_value
    return filter_func