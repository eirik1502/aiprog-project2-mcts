import games.game_simulator as simulator

ledge_board_small = [0, 1, 1, 0, 2]
ledge_board_from_notes = [0, 0, 0, 1, 0, 2, 0, 0, 1, 0]
ledge_board_large = [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 1]


config = simulator.BatchedGameSimulatorConfig()
config.batch_size = 30
config.print_full_tree_every_episode = False
config.print_full_tree_at_batch_end = False
config.print_tree_every_move = False
config.print_only_chosen_tree_nodes = True


config.verbose = True

config.simulations_per_move = 1000
config.starting_player = 0  # player 1 or 2 in the range [0, 1], -1 for random
config.game_type = simulator.GameType.LEDGE
config.ledge_initial_board = [0,1,0,1,0,1,0,1, 0,0,2,0,0,1,1,1]  # [0, 1, 2, 1, 0, 0, 1]

config.nim_initial_board_pieces = 50
config.nim_max_turn_pieces_remove = 10

simulator.perform_batch_run(config)
