from dataclasses import dataclass
from typing import Optional, OrderedDict, List

from mcts.mcts_core.state_manager import GameState
from mcts.mcts_core.utils import two_player_other_player


@dataclass(eq=True)
class TreeNodeChildEdge:
    q_value: float
    traversals: int
    eval: float

    def __str__(self):
        return f"[e={self.eval} t={self.traversals} q={'%.3f' % self.q_value}]"


class TreeNode:
    def __init__(self, state: GameState, next_player: Optional[int] = None, child: Optional['TreeNode'] = None):
        self.game_state = state  # read only
        self.visits = 0
        self.next_player = next_player  # automatically calculated if added as a child

        self.parent: Optional['TreeNode'] = None  # read only
        self.children_edges: OrderedDict['TreeNode', TreeNodeChildEdge] = OrderedDict[TreeNode, TreeNodeChildEdge]()
        if child is not None:
            self.add_child(child)

    def add_child(self, node: 'TreeNode'):
        self.children_edges[node] = TreeNodeChildEdge(
            q_value=0,
            traversals=0,
            eval=0
        )
        node.next_player = two_player_other_player(self.next_player)
        node.parent = self

    def get_children(self):
        return list(self.children_edges.keys())

    def get_children_edges(self):
        return list(self.children_edges.values())

    def get_edge_to_child(self, child: 'TreeNode'):
        if not child in self.children_edges:
            raise ValueError("trying to retrieve child edge of a non-existing child")
        return self.children_edges[child]

    def add_children(self, nodes: List['TreeNode']):
        for node in nodes:
            self.add_child(node)

    def copy_and_remove_tree(self):
        return TreeNode(self.game_state, next_player=self.next_player)

    def __str__(self):
        return f"(visits={self.visits} next_player={self.next_player} state={self.game_state})"

    def __repr__(self):
        return self.__str__()
