"""Example 44: pytest verification for Forcing B-Tree Splits Up to the Root."""

from example import BTree


def test_root_split_increases_height_by_exactly_one() -> None:
    tree = BTree(t=2)
    for key in range(1, 9):
        tree.insert(key)
    before = tree.height()
    tree.insert(9)
    assert tree.height() == before + 1


def test_split_root_has_exactly_two_children() -> None:
    tree = BTree(t=2)
    for key in range(1, 10):
        tree.insert(key)
    assert len(tree.root.children) == 2


# => Run: pytest -- Output: 2 passed
