"""Example 40: pytest verification for the Custom __iter__ Binary Tree Walk."""

from example import BinaryTree, Node


def test_for_loop_yields_values_in_sorted_order() -> None:
    tree: BinaryTree = BinaryTree(Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7))))
    assert [v for v in tree] == [1, 2, 3, 4, 6, 7]  # => in-order == sorted, for a BST


def test_empty_tree_yields_nothing() -> None:
    tree: BinaryTree = BinaryTree(None)
    assert list(tree) == []  # => no root -- the generator yields zero values


# => Run: pytest -- Output: 2 passed
