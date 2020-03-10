import random

from games.game_general import GameState
from games.mc_tree_funcs import DefaultPolicy
from games.state_manager import StateManager


class RandomDefaultPolicy(DefaultPolicy):
    def __init__(self, state_manager: StateManager):
        self._state_manager = state_manager

    def follow_policy(self, state: GameState) -> GameState:
        return random.choice(self._state_manager.get_successor_states(state))
