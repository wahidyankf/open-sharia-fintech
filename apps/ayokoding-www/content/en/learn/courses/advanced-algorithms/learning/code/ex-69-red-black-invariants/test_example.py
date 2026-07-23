"""Example 69: pytest verification for Red-Black Tree Invariants."""

import random

from example import Color, RedBlackTree, black_height, no_red_red_violation


def test_invariants_hold_after_random_inserts() -> None:
    random.seed(111)
    tree = RedBlackTree()
    values = list(range(150))
    random.shuffle(values)
    for v in values:
        tree.insert(v)
    assert no_red_red_violation(tree.root)
    assert black_height(tree.root) != -1
    assert tree.root is not None
    assert tree.root.color == Color.BLACK


def test_invariants_hold_after_ascending_inserts_the_bst_worst_case() -> None:
    tree = RedBlackTree()
    for v in range(100):
        tree.insert(v)
    assert no_red_red_violation(tree.root)
    assert black_height(tree.root) != -1


def test_single_insert_leaves_a_black_root() -> None:
    tree = RedBlackTree()
    tree.insert(42)
    assert tree.root is not None
    assert tree.root.color == Color.BLACK


# => Run: pytest -- Output: 3 passed
