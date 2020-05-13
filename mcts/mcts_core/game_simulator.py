import random
from dataclasses import dataclass
from typing import Tuple, List

from mcts.mcts_core.mc_default_policy import RandomDefaultPolicy
from mcts.mcts_core.mc_tree import TreeNode
from mcts.mcts_core.mc_tree_funcs import backprop_node_value, tree_search, print_tree, expand_node, \
    TreePolicy, DefaultPolicy, rollout, follow_most_traversed_child_edge
from mcts.mcts_core.mc_tree_policy import UctTreePolicy
from mcts.mcts_core.state_manager import StateManager, GameState


@dataclass(frozen=True)
class GameSimulatorConfig:
    game_state_manager: StateManager
    verbose: bool = True
    print_tree_every_move: bool = False
    simulations_per_move: int = 100
    starting_player: int = 0


@dataclass(frozen=True)
class BatchedGameSimulatorConfig(GameSimulatorConfig):
    batch_size: int = 10
    print_full_tree_every_episode: bool = False
    print_full_tree_at_batch_end: bool = False
    print_only_chosen_tree_nodes: bool = False


def rollout_evaluation(state_manager: StateManager, from_node: TreeNode, default_policy: DefaultPolicy) -> float:
    state = from_node.game_state
    player_won = rollout(state_manager, state, default_policy=default_policy)
    return 1 if player_won == 0 else -1


def perform_simulation(state_manager, root_node, tree_policy: TreePolicy, default_policy: DefaultPolicy):
    """
    Modifies the tree given by the root_node
    """
    leaf = tree_search(root_node, tree_policy=tree_policy)
    is_terminal = not expand_node(state_manager, leaf)

    # pick an expanded node for rollout evaluation or the prior leaf node if it is terminal
    eval_node = random.choice(leaf.get_children()) if not is_terminal else leaf

    value = rollout_evaluation(state_manager, eval_node, default_policy=default_policy)
    backprop_node_value(eval_node, value, root_node=root_node)  # the root node might have parents that we dont care about


def perform_episode(config: GameSimulatorConfig) -> Tuple[List[GameState], List[TreeNode]]:
    simulations_per_move = config.simulations_per_move
    verbose = config.verbose
    do_print_tree = config.print_tree_every_move
    starting_player = config.starting_player if (0 <= config.starting_player <= 1) else random.randint(0, 1)

    state_manager = config.game_state_manager  # _create_state_manager(config, override_starting_player=starting_player) if state_manager is None else state_manager
    tree_policy = UctTreePolicy(uct_c=1)
    default_policy = RandomDefaultPolicy(state_manager=state_manager)

    absolute_root_node = TreeNode(state_manager.get_initial_state(), next_player=starting_player)
    curr_root_node = absolute_root_node
    state_history = []  # the state history of the actual game played
    root_history = []

    while True:
        state_history.append(curr_root_node.game_state)
        root_history.append(curr_root_node)

        if verbose:
            prev_state = state_history[-2] if len(state_history) >= 2 else None
            action_str = state_manager.action_str(state_history[-1], prev_state)
            print(action_str)

        if state_manager.is_terminal_state(curr_root_node.game_state):
            break

        for i in range(simulations_per_move):
            perform_simulation(state_manager, curr_root_node, tree_policy, default_policy)

        # choose next root node
        # corresponding to making an actual move
        next_root_node_in_tree = follow_most_traversed_child_edge(curr_root_node)
        next_root_node = next_root_node_in_tree.copy_and_remove_tree()

        if do_print_tree:
            print_tree(curr_root_node, highlight_nodes=[next_root_node_in_tree])

        curr_root_node = next_root_node

    return state_history, root_history


def perform_batch_run(config: BatchedGameSimulatorConfig) -> Tuple[float, List[List[GameState]], List[List[TreeNode]]]:
    print_full_tree_every_episode = config.print_full_tree_every_episode
    print_full_tree_at_end = config.print_full_tree_at_batch_end
    print_only_chosen_tree_nodes = config.print_only_chosen_tree_nodes

    games_history = []
    games_root_history = []

    for i in range(config.batch_size):
        print(f"Starting batch {i}")
        state_history, root_node_history = perform_episode(config)
        games_history.append(state_history)
        games_root_history.append(root_node_history)

        if print_full_tree_every_episode:
            print_tree(root_node_history[0], highlight_nodes=root_node_history, print_only_highlighted=print_only_chosen_tree_nodes)

    if print_full_tree_at_end:
        last_root_node_history = games_root_history[-1]
        print_tree(last_root_node_history[0], highlight_nodes=last_root_node_history, print_only_highlighted=print_only_chosen_tree_nodes)

    # a state manager to evaluate player_won, hence starting player is not important
    state_manager = config.game_state_manager

    total_games = len(games_history)
    p2_wins = sum([
        state_manager.player_won(game[-1])
        for game in games_history
    ])
    p1_wins = total_games - p2_wins
    p1_win_percentage = p1_wins / total_games

    print(f"Player 1 wins {p1_wins} of {total_games} ({p1_win_percentage})")

    return p1_win_percentage, games_history, games_root_history


if __name__ == '__main__':
    pass
