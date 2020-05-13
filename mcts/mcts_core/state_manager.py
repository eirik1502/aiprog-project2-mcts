from abc import ABC, abstractmethod
from typing import List, Optional, Any


GameState = Any


class StateManager(ABC):

    @abstractmethod
    def get_initial_state(self) -> GameState:
        pass

    @abstractmethod
    def get_successor_states(self, state: GameState) -> List[GameState]:
        pass

    @abstractmethod
    def is_terminal_state(self, state: GameState) -> bool:
        pass

    @abstractmethod
    def player_won(self, state: GameState) -> int:
        pass

    @abstractmethod
    def action_str(self, state: GameState, previous_state: Optional[GameState]) -> str:
        pass
