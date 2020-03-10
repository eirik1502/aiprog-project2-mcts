import random
from dataclasses import dataclass
from typing import Tuple, List, Optional

from games.game_general import Game, GameState, other_player
from games.state_manager import StateManager


@dataclass(eq=True, frozen=True)
class NimState(GameState):
    num_pieces: int = -1
    player: int = -1  # should be the non-starting player when in initial_state
    initial_state: bool = False


class NimStateManager(StateManager):

    def __init__(self, num_pieces: int, max_turn_pieces_remove: int, player_start: int):
        self._num_pieces = num_pieces
        self._max_turn_pieces_remove = max_turn_pieces_remove
        self._player_start = player_start

    def get_initial_state(self) -> NimState:
        return NimState(
            num_pieces=self._num_pieces,
            player=other_player(self._player_start),  # should be the non-starting player when in initial_state
            initial_state=True
        )

    def get_successor_states(self, state: NimState) -> List[NimState]:
        curr_state = state
        return [
            NimState(
                num_pieces=next_num_pieces,
                player=other_player(curr_state.player),
                initial_state=False
            )
            for next_num_pieces in [
                curr_state.num_pieces - remove_pieces
                for remove_pieces in range(1, self._max_turn_pieces_remove + 1)
            ]
            if next_num_pieces >= 0
        ]

    def is_terminal_state(self, state: NimState) -> bool:
        return state.num_pieces <= 0

    def player_won(self, state: NimState) -> int:
        if self.is_terminal_state(state):
            return state.player
        else:
            return -1

    def action_str(self, state: NimState, previous_state: Optional[NimState] = None) -> str:
        if state.initial_state:
            return f"Start Pile: {state.num_pieces} stones"
        else:
            if previous_state is None:
                raise ValueError("Cannot create action str when previous state is not given and not in intial state")

            s = f"Player {state.player + 1} selects {previous_state.num_pieces - state.num_pieces}: Remaining stones = {state.num_pieces}"

            if self.is_terminal_state(state):
                s += f"\nPlayer {self.player_won(state) + 1} wins"

            return s

if __name__ == '__main__':
    def testRandomPlaythrough():
        nim = NimStateManager(10, 3, 0)
        state = nim.get_initial_state()
        previous_state = None
        print(nim.action_str(state, previous_state))
        while not nim.is_terminal_state(state):
            successor_states = nim.get_successor_states(state)

            previous_state = state
            state = random.choice(successor_states)

            print(nim.action_str(state, previous_state))

    testRandomPlaythrough()
