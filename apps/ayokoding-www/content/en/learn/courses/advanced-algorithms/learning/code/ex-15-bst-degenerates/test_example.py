"""Example 15: pytest verification for BST Degeneration on Sorted Input."""

from example import Node, height, insert


def test_ascending_inserts_produce_height_n_minus_1() -> None:
    root: Node | None = None
    for k in range(10):
        root = insert(root, k)
    assert height(root) == 9  # => 10 nodes, all in one chain -- height n-1


def test_balanced_insert_order_produces_much_smaller_height() -> None:
    root: Node | None = None
    for k in [8, 4, 12, 2, 6, 10, 14, 1, 3, 5]:  # => a level-order, balanced sequence
        root = insert(root, k)
    assert height(root) < 9  # => far shorter than the degenerate chain's height


# => Run: pytest -- Output: 2 passed
