import math

from mcts.mcts_core.mc_tree import TreeNode
from mcts.mcts_core.mc_tree_funcs import TreePolicy
from mcts.mcts_core.utils import max_with_probabilities, min_with_probabilities


def uct(const, visits, edge_traversals):
    log_visits = math.log2(visits) if visits != 0 else 0
    return const * math.sqrt(log_visits / (1 + edge_traversals))


class UctTreePolicy(TreePolicy):
    def __init__(self, uct_c):
        self.uct_c = uct_c

    def follow_policy(self, node: TreeNode) -> TreeNode:
        if node.next_player is None or not (0 <= node.next_player <= 1):
            raise ValueError("nodes next player is not assigned")

        next_player = node.next_player
        uct_sign = 1 if next_player == 0 else -1
        children = node.get_children()
        probabilities = [
            q_value + uct_sign * uct(self.uct_c, node.visits, edge_traversals)
            for q_value, edge_traversals in
            [
                (edge.q_value, edge.traversals)
                for (child, edge) in zip(children, node.get_children_edges())
            ]
        ]
        pick_child_with_prob_func = max_with_probabilities if next_player == 0 else min_with_probabilities
        node = pick_child_with_prob_func(children, probabilities)
        return node
