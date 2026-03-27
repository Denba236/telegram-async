from typing import Optional, Dict, List, Union


class State:
    """A single FSM state"""

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
    """Metaclass for StatesGroup to automatically collect states"""

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # Collect all states from the class
        states = {}
        for key, value in namespace.items():
            if isinstance(value, State):
                value.group = cls
                states[key] = value
            elif isinstance(value, StatesGroupMeta):
                # For nested groups
                for state_name, state in value._states.items():
                    states[f"{value.__name__}.{state_name}"] = state

        cls._states = states
        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    """
    A group of FSM states

    Example:
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
        """Gets a state by name"""
        return cls._states.get(name)

    @classmethod
    def all_states(cls) -> List[State]:
        """Returns all states in the group"""
        return list(cls._states.values())

    @classmethod
    def has_state(cls, state: Union[str, State]) -> bool:
        """Checks if a state belongs to the group"""
        state_str = str(state) if isinstance(state, State) else state
        return any(str(s) == state_str or s.name == state_str for s in cls._states.values())
