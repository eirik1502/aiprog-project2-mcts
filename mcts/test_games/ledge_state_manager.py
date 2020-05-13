import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

from mcts.mcts_core.state_manager import StateManager, GameState


@dataclass(frozen=True)
class LedgeGameConfig:
    initial_board: List[int] = (0, 0, 1, 0, 1, 0, 2)
    starting_player: int = 0


@dataclass(frozen=True)
class LedgeState:
    initial_state: bool
    board: Tuple[int, ...]
    coin_pick: int  # -1 if no coin was picked
    player: int  # when in initial state, player should be opposite of the starting player


class LedgeStateManager(StateManager):
    def __init__(self, config: LedgeGameConfig):
        self._initial_board = tuple(config.initial_board)
        self._starting_player = config.starting_player

    @staticmethod
    def __other_player(player: int) -> int:
        return (player + 1) % 2

    def get_initial_state(self) -> GameState:
        return LedgeState(
            initial_state=True,
            board=self._initial_board,
            coin_pick=-1,
            player=self.__other_player(self._starting_player)
        )

    def get_successor_states(self, state: LedgeState) -> List[GameState]:
        successor_states = []
        next_player = self.__other_player(state.player)

        # successor state when picking coin
        if state.board[0] != 0:
            coin_pick = state.board[0]
            successor_states.append(LedgeState(
                initial_state=False,
                board=(0,) + state.board[1:],
                coin_pick=coin_pick,
                player=next_player
            ))

        # successor states when moving coins
        prev_coin_index = -1
        for coin_index, coin_type in enumerate(state.board):
            if coin_type != 0:
                # find positions where the coin can be moved
                for move_coin_next_index in range(coin_index - 1, prev_coin_index, -1):
                    next_board = list(state.board)
                    next_board[coin_index] = 0  # no coin
                    next_board[move_coin_next_index] = coin_type
                    successor_states.append(LedgeState(
                        initial_state=False,
                        board=tuple(next_board),
                        coin_pick=-1,
                        player=next_player
                    ))

                prev_coin_index = coin_index
        return successor_states

    def is_terminal_state(self, state: LedgeState) -> bool:
        return state.coin_pick == 2

    def player_won(self, state: LedgeState) -> int:
        if self.is_terminal_state(state):
            return state.player
        else:
            return -1

    def action_str(self, state: LedgeState, previous_state: Optional[LedgeState]) -> str:
        state_player = state.player
        if state.initial_state:
            return f"Start Board: {state.board}"
        elif state.coin_pick == 1:
            return f"Player {state_player} picks up copper: {state.board}"
        elif state.coin_pick == 2:
            return f"Player {state_player} picks up gold: {state.board}\nPlayer {state_player} wins"
        else:
            # a coin was moved
            cell1 = -1
            cell2 = -1
            moved_coin_type = -1
            for coin_index, (coin_type, prev_coin_type) in enumerate(zip(state.board, previous_state.board)):
                if coin_type != prev_coin_type:
                    if cell1 == -1:
                        moved_coin_type = coin_type
                        cell1 = coin_index
                    else:
                        cell2 = coin_index
                        break

            coin_type_str = "gold" if moved_coin_type == 2 else "copper"
            return f"player {state_player} moves {coin_type_str} from cell {cell2} to {cell1}: {state.board}"


if __name__ == '__main__':

    def test_successor_states():
        initial_board = [1, 0, 0, 1, 0, 2, 1]
        state_manager = LedgeStateManager(initial_board, 0)
        initial_state = state_manager.get_initial_state()
        state = initial_state
        print(state)
        for state in state_manager.get_successor_states(state):
            print(f"initial state:\n{initial_state}")
            print(state)


    def test_terminal():
        state_manager = LedgeStateManager()
        states = [
            LedgeState((0, 0, 1), 2, 0),
            LedgeState((0, 0, 1), 2, 1),
            LedgeState((2, 0, 0), -1, 0)
        ]
        for state in states:
            print(state_manager.is_terminal_state(state))
            print(state_manager.player_won(state))


    def random_run():
        state_manager = LedgeStateManager((0, 0, 1, 0, 1, 2), 0)
        init_state = state_manager.get_initial_state()
        state = init_state
        print(f"initial state: {init_state}")
        while not state_manager.is_terminal_state(state):
            successor_states = state_manager.get_successor_states(state)
            pick_state = random.choice(successor_states)
            print(f"successors: {successor_states} \npicked: {pick_state}")
            state = pick_state
        print(f"player won: {state_manager.player_won(state)}")


    def random_run_verbose():
        state_manager = LedgeStateManager((0, 0, 1, 0, 1, 2), 0)
        init_state = state_manager.get_initial_state()
        state = init_state
        previous_state = None
        print(state_manager.action_str(state, previous_state))
        while not state_manager.is_terminal_state(state):
            successor_states = state_manager.get_successor_states(state)
            previous_state = state
            state = random.choice(successor_states)
            print(state_manager.action_str(state, previous_state))


    random_run_verbose()
