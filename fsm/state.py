from typing import Optional, Dict, List, Union, Type


class State:
    """Pojedynczy stan FSM"""

    def __init__(self, name: str, group: Optional['StatesGroup'] = None):
        self.name = name
        self.group = group

    def __repr__(self):
        if self.group:
            return f"State('{self.group.__name__}:{self.name}')"
        return f"State('{self.name}')"

    def __eq__(self, other):
        if isinstance(other, State):
            return self.name == other.name and self.group == other.group
        elif isinstance(other, str):
            return str(self) == other or self.name == other
        return False

    def __str__(self):
        if self.group:
            return f"{self.group.__name__}:{self.name}"
        return self.name


class StatesGroupMeta(type):
    """Metaklasa dla StatesGroup do automatycznego zbierania stanów"""

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Zbierz wszystkie stany z klasy
        states = {}
        for key, value in namespace.items():
            if isinstance(value, State):
                value.group = cls
                states[key] = value
            elif isinstance(value, StatesGroupMeta):
                # Dla zagnieżdżonych grup
                for state_name, state in value._states.items():
                    states[f"{value.__name__}.{state_name}"] = state

        cls._states = states
        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    """
    Grupa stanów FSM

    Przykład:
        class OrderStates(StatesGroup):
            name = State("name")
            address = State("address")
            payment = State("payment")

        @dp.message(State(OrderStates.name))
        async def process_name(ctx):
            pass
    """

    _states: Dict[str, State] = {}

    @classmethod
    def get_state(cls, name: str) -> Optional[State]:
        """Pobiera stan po nazwie"""
        return cls._states.get(name)

    @classmethod
    def all_states(cls) -> List[State]:
        """Zwraca wszystkie stany w grupie"""
        return list(cls._states.values())

    @classmethod
    def has_state(cls, state: Union[str, State]) -> bool:
        """Sprawdza czy stan należy do grupy"""
        state_str = str(state) if isinstance(state, State) else state
        return any(str(s) == state_str or s.name == state_str for s in cls._states.values())