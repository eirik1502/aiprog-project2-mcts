import mcts.mcts_core.game_simulator as mcts
from mcts.test_games.ledge_state_manager import LedgeGameConfig, LedgeStateManager

print("Running test games")


def run_ledge():
    ledge_board_small = [0, 1, 1, 0, 2]
    ledge_board_from_notes = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
    ledge_board_large = [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 1]
    ledge_board_another_test = [0, 1, 2, 1, 0, 0, 1]
    ledge_board_last_test = [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 1, 1]

    starting_player = 1

    ledge_state_manager = LedgeStateManager(LedgeGameConfig(
        initial_board=ledge_board_another_test,
        starting_player=starting_player
    ))

    mcts_config = mcts.BatchedGameSimulatorConfig(
        game_state_manager=ledge_state_manager,
        verbose=True,
        print_tree_every_move=False,
        simulations_per_move=500,
        starting_player=starting_player,
        batch_size=100,
        print_full_tree_every_episode=False,
        print_full_tree_at_batch_end=False,
        print_only_chosen_tree_nodes=False
    )
    # config.batch_size = 30
    # config.simulations_per_move = 1000
    # config.starting_player = 0  # player 1 or 2 in the range [0, 1], -1 for random


    # config.nim_initial_board_pieces = 50
    # config.nim_max_turn_pieces_remove = 10
    #
    mcts.perform_batch_run(mcts_config)


run_ledge()
