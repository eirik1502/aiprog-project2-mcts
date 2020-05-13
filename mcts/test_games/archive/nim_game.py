import random
from dataclasses import dataclass
from typing import List

from games.game_general import Game
from games.nim_state_manager import NimState


@dataclass(eq=True, frozen=True)
class NimAction:
    num_pieces: int


class Nim(Game):

    def __init__(self, num_pieces: int, max_turn_pieces_remove: int, player_start: int = -1, copy_of: Optional['Nim'] = None):
        if copy_of is not None:
            self._max_turn_pieces_remove = copy_of._max_turn_pieces_remove
            self._states = copy_of._states

        else:
            if player_start >= 2:
                raise Exception("player_start should be negative indicating random or in the range [0, 1]")

            if num_pieces < 0:
                raise Exception("Nim cannot start with negative amount of pieces")

            if player_start < 0:
                player_start = random.randint(0, 1)

            self._max_turn_pieces_remove = max_turn_pieces_remove
            self._states = [NimState(player_start if num_pieces <= 0 else -1, num_pieces, player_start)]

    def copy(self) -> 'Nim':
        return Nim(copy_of=self)

    def get_state(self) -> NimState:
        return self._states[-1]

    def get_successor_states(self) -> List[NimState]:
        curr_state = self.get_state()
        return [
            NimState(
                player_won=curr_state.next_player if next_num_pieces == 0 else -1,
                num_pieces=next_num_pieces,
                next_player=(curr_state.next_player + 1) % 2
            )
            for next_num_pieces in [
                curr_state.num_pieces - remove_pieces
                for remove_pieces in range(1, self._max_turn_pieces_remove + 1)
            ]
            if next_num_pieces >= 0
        ]

    def apply_next_state(self, state: NimState):
        curr_state = self.get_state()

        if curr_state.is_terminal():
            raise Exception("Cannot transition into new state, a player has already won")

        if not 1 <= curr_state.num_pieces - state.num_pieces <= self._max_turn_pieces_remove:
            raise ValueError("cannot transition into the given state, num_pieces invalid")

        if curr_state.next_player == state.next_player:
            raise ValueError("Cannot transition into new state, same player is assigned as next")

        self._states.append(state)

    def perform_action(self, action: NimAction):
        curr_state = self.get_state()

        next_num_pieces = curr_state.num_pieces - action.num_pieces
        next_state = NimState(
            player_won=curr_state.next_player if next_num_pieces <= 0 else -1,
            num_pieces=next_num_pieces,
            next_player=(curr_state.next_player + 1) % 2
        )

        self.apply_next_state(next_state)

    def __str__(self):
        return f"[Nim {self.get_state()}]"

    def __repr__(self):
        return self.__str__()


# for testing
if __name__ == '__main__':
    def testDataClass():
        a1 = NimAction(3)
        a2 = NimAction(2)
        a3 = NimAction(3)

        print(a1 == a2)
        print(a1 == a3)
        print({a1, a2, a3})

    def testSimpleNim():
        nim = Nim(10, 3, 0)
        print(nim)
        nim.perform_action(NimAction(3))
        print(nim)
        nim.perform_action(NimAction(1))
        print(nim)
        nim.perform_action(NimAction(3))
        print(nim)
        nim.perform_action(NimAction(3))
        print(nim)

    def testRandomPlaythrough():
        nim = Nim(10, 3, 0)
        while not nim.get_state().is_terminal():
            successor_states = nim.get_successor_states()
            pick_next_state = random.choice(successor_states)
            print(f"chose state {pick_next_state} from possible states: {successor_states}")
            nim.apply_next_state(pick_next_state)

        print(f"final state: {nim}")

    testRandomPlaythrough()