from typing import List


def two_player_other_player(player: int) -> int:
    return (player + 1) % 2


def max_with_probabilities(elements: List[any], probabilities: List[float]):
    return max(zip(elements, probabilities), key=lambda elem_prob: elem_prob[1])[0]


def min_with_probabilities(elements: List[any], probabilities: List[float]):
    return min(zip(elements, probabilities), key=lambda elem_prob: elem_prob[1])[0]


def repeat_str(length, s):
    return "".join([s for i in range(length)])

def spaces_of_len(length: int) -> str:
    return "".join([" " for i in range(length)])

def fixed_size_str_center(length: int, s: str, fill=" ") -> str:
    if len(s) > length:
        return s

    spaces_before = int((length - len(s)) / 2)
    spaces_after = length - len(s) - spaces_before
    return repeat_str(spaces_before, fill) + s + repeat_str(spaces_after, fill)
