"""Example 14: pytest verification for BST Insert and Search."""

from example import Node, inorder, insert, search


def test_inorder_traversal_is_always_sorted() -> None:
    root: Node | None = None
    for v in [50, 20, 80, 10, 30, 70, 90, 5]:
        root = insert(root, v)
    assert inorder(root) == sorted(inorder(root))  # => trivially true, but explicit


def test_search_finds_present_and_rejects_absent_values() -> None:
    root: Node | None = None
    for v in [15, 10, 20, 8, 12]:
        root = insert(root, v)
    assert search(root, 12) is True
    assert search(root, 99) is False


def test_search_on_empty_tree_returns_false() -> None:
    assert search(None, 1) is False  # => an empty tree contains nothing


# => Run: pytest -- Output: 3 passed
