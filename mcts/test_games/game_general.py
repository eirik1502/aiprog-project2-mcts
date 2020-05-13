from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class GameState(ABC):
    pass


class Game(ABC):

    @abstractmethod
    def get_state(self) -> GameState:
        pass

    @abstractmethod
    def get_successor_states(self) -> List[GameState]:
        pass

    @abstractmethod
    def copy(self) -> 'Game':
        pass


def other_player(player: int) -> int:
    return (player + 1) % 2
