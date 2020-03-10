import math
import random
from abc import ABC, abstractmethod
from typing import Optional, Callable, Union, List

from games.game_general import GameState
from games.mc_tree import TreeNode, TreeNodeChildEdge
from games.state_manager import StateManager
from games.utils import max_with_probabilities, min_with_probabilities, repeat_str, fixed_size_str_center


class TreePolicy(ABC):
    @abstractmethod
    def follow_policy(self, node: TreeNode) -> TreeNode:
        pass


class DefaultPolicy(ABC):
    @abstractmethod
    def follow_policy(self, state: GameState) -> GameState:
        pass


def backprop_node_value(from_child_node: TreeNode, value: float, root_node: Optional[TreeNode] = None):
    """Mutates the tree"""
    node = from_child_node
    prev_node: Optional[TreeNode] = None  # needed to retrieve the right edge
    while True:
        node.visits += 1
        if prev_node is not None:
            # update edge to child
            edge = node.get_edge_to_child(prev_node)
            edge.traversals += 1
            edge.eval += value
            edge.q_value = edge.eval / edge.traversals

        if node.parent is None or (root_node is not None and node == root_node):
            break
        else:
            prev_node = node
            node = node.parent


def follow_most_traversed_child_edge(node: TreeNode) -> TreeNode:
    if node.next_player is None or not (0 <= node.next_player <= 1):
        raise ValueError("nodes next player is not assigned")

    children = node.get_children()
    probabilities = [
        edge.traversals
        for edge in node.get_children_edges()
    ]
    node = max_with_probabilities(children, probabilities)
    return node


def tree_search(root_node: TreeNode, tree_policy: TreePolicy) -> TreeNode:
    node = root_node
    while len(node.get_children()) > 0:
        node = tree_policy.follow_policy(node)

    return node


def expand_node(state_manager: StateManager, node: TreeNode) -> bool:
    """
    Finds all child nodes and adds them to the given node, if the node is not a final state
    Returns: true if children were added else false
    """
    if len(node.get_children()) != 0:
        raise ValueError("Should not expand node that already has children")
    if state_manager.is_terminal_state(node.game_state):
        return False
    else:
        next_states = state_manager.get_successor_states(node.game_state)
        children = [
            TreeNode(state)
            for state in next_states
        ]
        node.add_children(children)
        return True


def rollout(state_manager: StateManager, start_state: GameState, default_policy: DefaultPolicy) -> int:
    state = start_state
    while not state_manager.is_terminal_state(state):
        state = default_policy.follow_policy(state)
    return state_manager.player_won(state)


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = "\033[33m"


def tree_str(
        node: TreeNode,
        edge: Optional[TreeNodeChildEdge] = None,
        level=0,
        highlight_nodes: Union[None, TreeNode, List[TreeNode]] = None,
        print_only_highlighted: bool = False
):
    indent_len = 25
    edge_str = edge.__str__() if edge is not None else ""
    highlight_this_node = highlight_nodes is not None and (
        (isinstance(highlight_nodes, TreeNode) and highlight_nodes == node)
        or (isinstance(highlight_nodes, list) and node in highlight_nodes)
    )
    s = ""
    if print_only_highlighted and not highlight_this_node:
        return s

    s += "\n" + repeat_str((level-1), repeat_str(indent_len, " ")) \
        + ("|" + fixed_size_str_center(indent_len-2, edge_str, "_") + " " if level != 0 else "") \
        + (node.__str__() if not highlight_this_node else f"{Bcolors.YELLOW}{node.__str__()}{Bcolors.ENDC}")

    for child, edge in zip(node.get_children(), node.get_children_edges()):
        s += tree_str(child, edge=edge, level=level+1, highlight_nodes=highlight_nodes, print_only_highlighted=print_only_highlighted)

    return s


def print_tree(node: TreeNode, highlight_nodes: Union[None, TreeNode, List[TreeNode]] = None, print_only_highlighted: bool = False):
    print("\n----- MC tree -----\n" + tree_str(node, highlight_nodes=highlight_nodes, print_only_highlighted=print_only_highlighted))


if __name__ == '__main__':
    def test_tree_search_random():
        # build tree
        root = TreeNode(None)
        existing_nodes = [root]
        for i in range(10):
            node = TreeNode(None)
            add_to = random.choice(existing_nodes)
            add_to.add_child(node)
            existing_nodes.append(node)

        print_tree(root)

        expand_node = tree_search(root)

        print_tree(root, highlight_nodes=expand_node)

    def build_tree():
        # build tree
        root = TreeNode(None)
        r1 = TreeNode(None)
        r2 = TreeNode(None)
        r1n1 = TreeNode(None)
        r1n2 = TreeNode(None)
        r2n1 = TreeNode(None)
        r2n2 = TreeNode(None)
        root.add_children([r1, r2])
        r1.add_children([r1n1, r1n2])
        r2.add_children([r2n1, r2n2])
        return root

    def test_tree_search():
        root = build_tree()
        r2 = root.get_children()[1]
        r2n1 = r2.get_children()[0]
        r2n2 = r2.get_children()[1]
        r2.get_children_edges()[0].traversals = 2
        root.get_children_edges()[1].q_value = 0.2
        r2n1.visits = 5
        r2n2.visits = 5

        expand_node = tree_search(root)
        print_tree(root, highlight_node=expand_node)

    def test_backprop():
        root = build_tree()

        for i in range(31):
            expand_node = tree_search(root)
            backprop_node_value(expand_node, random.randint(-1, 1))
            if i % 3 == 0:
                print_tree(root, highlight_node=expand_node)


    test_backprop()