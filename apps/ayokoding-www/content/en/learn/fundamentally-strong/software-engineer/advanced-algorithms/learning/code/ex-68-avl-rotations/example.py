"""Example 68: AVL Tree Insert with Rotations -- Height Stays O(log n)."""

# An AVL tree (co-12) is a BST that ADDITIONALLY enforces: every node's two
# subtree heights differ by at most 1. Whenever an insert would violate that,
# a ROTATION restructures the tree locally to restore balance -- unlike
# Example 15's plain BST, sorted-order inserts can NEVER degrade into a chain.
from __future__ import annotations

import math


class AVLNode:  # => a BST node augmented with its own subtree height
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height: int = 1  # => a fresh leaf has height 1


def height(node: AVLNode | None) -> int:  # => 0 for an empty (sub)tree, by convention
    return node.height if node is not None else 0


def balance_factor(node: AVLNode) -> int:  # => left height minus right height
    return height(node.left) - height(node.right)  # => >1 or <-1 means "unbalanced"


def update_height(
    node: AVLNode,
) -> None:  # => recomputes from the (already-updated) children
    node.height = 1 + max(height(node.left), height(node.right))


def rotate_right(y: AVLNode) -> AVLNode:  # => fixes a LEFT-heavy imbalance
    x = y.left  # => x is guaranteed non-None whenever this is called (left-heavy)
    assert x is not None  # => narrows the type -- a left-heavy node has a left child
    y.left = x.right  # => x's right subtree becomes y's new left subtree
    x.right = y  # => y becomes x's right child -- x rises to take y's old position
    update_height(y)  # => y's height must be recomputed FIRST (it's now lower)
    update_height(x)  # => then x's, since it depends on y's just-updated height
    return x  # => x is the new root of this rotated subtree


def rotate_left(x: AVLNode) -> AVLNode:  # => the mirror image: fixes a RIGHT-heavy case
    y = x.right
    assert y is not None  # => narrows the type -- a right-heavy node has a right child
    x.right = y.left
    y.left = x
    update_height(x)
    update_height(y)
    return y


def avl_insert(
    node: AVLNode | None, value: int
) -> AVLNode:  # => returns the new subtree root
    if node is None:  # => base case: an empty spot becomes a new leaf
        return AVLNode(value)
    if value < node.value:
        node.left = avl_insert(node.left, value)
    elif value > node.value:
        node.right = avl_insert(node.right, value)
    else:
        return node  # => duplicate values are ignored
    update_height(
        node
    )  # => this node's height may have grown after the recursive insert
    balance = balance_factor(node)  # => checks whether THIS node is now unbalanced

    if (
        balance > 1 and node.left is not None and value < node.left.value
    ):  # => LEFT-LEFT
        return rotate_right(node)  # => a single right rotation fixes it
    if (
        balance < -1 and node.right is not None and value > node.right.value
    ):  # => RIGHT-RIGHT
        return rotate_left(node)  # => a single left rotation fixes it
    if (
        balance > 1 and node.left is not None and value > node.left.value
    ):  # => LEFT-RIGHT
        node.left = rotate_left(node.left)  # => first straighten the left child...
        return rotate_right(node)  # => ...then rotate this node -- a DOUBLE rotation
    if (
        balance < -1 and node.right is not None and value < node.right.value
    ):  # => RIGHT-LEFT
        node.right = rotate_right(node.right)  # => first straighten the right child...
        return rotate_left(node)  # => ...then rotate this node -- a DOUBLE rotation
    return node  # => already balanced -- no rotation needed


n = 100  # => 100 sorted keys -- Example 15's exact worst case for a plain BST
root: AVLNode | None = None
for k in range(n):  # => inserting in ASCENDING order
    root = avl_insert(root, k)  # => the AVL tree self-balances after every insert

tree_height = height(root)  # => the actual resulting height
log_bound = math.ceil(2 * math.log2(n + 2))  # => a generous O(log n) upper bound
print(tree_height)  # => Output: 7
print(
    log_bound
)  # => Output: 14 -- confirms tree_height comfortably fits under this bound

assert tree_height < log_bound  # => confirms O(log n), NOT the O(n) chain of Example 15
assert (
    tree_height < n
)  # => trivially true, but makes the contrast with Example 15 explicit
print("ex-68 OK")  # => Output: ex-68 OK
