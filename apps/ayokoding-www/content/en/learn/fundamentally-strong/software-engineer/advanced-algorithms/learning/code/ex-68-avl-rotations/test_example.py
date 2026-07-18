"""Example 68: pytest verification for AVL Rotations."""

import math

from example import AVLNode, avl_insert, height


def test_sorted_inserts_stay_logarithmic_height() -> None:
    root: AVLNode | None = None
    n = 200
    for k in range(n):
        root = avl_insert(root, k)
    bound = math.ceil(2 * math.log2(n + 2))
    assert height(root) < bound  # => far below the O(n) chain a plain BST would form


def test_balance_stays_within_one_after_every_insert() -> None:
    root: AVLNode | None = None
    for k in [10, 20, 30, 40, 50, 25]:  # => a mix that would unbalance a plain BST
        root = avl_insert(root, k)

    def check_balanced(node: AVLNode | None) -> bool:
        if node is None:
            return True
        diff = height(node.left) - height(node.right)
        return (
            abs(diff) <= 1 and check_balanced(node.left) and check_balanced(node.right)
        )

    assert check_balanced(root) is True


# => Run: pytest -- Output: 2 passed
