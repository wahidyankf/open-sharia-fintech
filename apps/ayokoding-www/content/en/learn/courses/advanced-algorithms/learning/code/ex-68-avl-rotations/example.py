"""Example 68: AVL Tree Insert with Rotations -- Height Stays O(log n)."""

# An AVL tree (co-12) is a BST that ADDITIONALLY enforces: every node's two
# subtree heights differ by at most 1. Whenever an insert would violate that,
# a ROTATION restructures the tree locally to restore balance -- unlike
# Example 15's plain BST, sorted-order inserts can NEVER degrade into a chain.
from __future__ import annotations  # => lets AVLNode reference itself in type hints

import math  # => log2/ceil, used only to compute the expected O(log n) upper bound


class AVLNode:  # => a BST node augmented with its own subtree height
    def __init__(self, value: int) -> None:  # => a fresh leaf node
        self.value = value  # => this node's key
        self.left: AVLNode | None = None  # => no left child yet
        self.right: AVLNode | None = None  # => no right child yet
        self.height: int = 1  # => a fresh leaf has height 1


def height(node: AVLNode | None) -> int:  # => 0 for an empty (sub)tree, by convention
    return (  # => opens the None-safe height lookup
        node.height if node is not None else 0  # => 0 stands in for an empty subtree
    )  # => avoids a None-check at every call site


def balance_factor(node: AVLNode) -> int:  # => left height minus right height
    return height(node.left) - height(node.right)  # => >1 or <-1 means "unbalanced"


def update_height(  # => recomputes a node's height from its children's already-updated heights
    node: AVLNode,  # => the node whose height needs recomputing
) -> None:  # => recomputes from the (already-updated) children
    node.height = 1 + max(  # => opens the taller-child height computation
        height(node.left),  # => the left child's own current height
        height(node.right),  # => both children's own current heights
    )  # => 1 plus the TALLER child


def rotate_right(y: AVLNode) -> AVLNode:  # => fixes a LEFT-heavy imbalance
    x = y.left  # => x is guaranteed non-None whenever this is called (left-heavy)
    assert x is not None  # => narrows the type -- a left-heavy node has a left child
    y.left = x.right  # => x's right subtree becomes y's new left subtree
    x.right = y  # => y becomes x's right child -- x rises to take y's old position
    update_height(y)  # => y's height must be recomputed FIRST (it's now lower)
    update_height(x)  # => then x's, since it depends on y's just-updated height
    return x  # => x is the new root of this rotated subtree


def rotate_left(x: AVLNode) -> AVLNode:  # => the mirror image: fixes a RIGHT-heavy case
    y = x.right  # => y is guaranteed non-None whenever this is called (right-heavy)
    assert y is not None  # => narrows the type -- a right-heavy node has a right child
    x.right = y.left  # => y's left subtree becomes x's new right subtree
    y.left = x  # => x becomes y's left child -- y rises to take x's old position
    update_height(x)  # => x's height must be recomputed FIRST (it's now lower)
    update_height(y)  # => then y's, since it depends on x's just-updated height
    return y  # => y is the new root of this rotated subtree


def avl_insert(  # => standard BST insert, then rebalances on the way back up
    node: AVLNode | None,  # => the current subtree root, or None if empty here
    value: int,  # => the current subtree root and the key to insert
) -> AVLNode:  # => returns the new subtree root
    if node is None:  # => base case: an empty spot becomes a new leaf
        return AVLNode(value)  # => a brand-new leaf, height 1
    if value < node.value:  # => belongs in the LEFT subtree
        node.left = avl_insert(  # => opens the left-subtree recursive insert
            node.left, value
        )  # => recurses, then re-attaches the result
    elif value > node.value:  # => belongs in the RIGHT subtree
        node.right = avl_insert(  # => opens the right-subtree recursive insert
            node.right, value
        )  # => recurses, then re-attaches the result
    else:  # => value already exists in the tree
        return node  # => duplicate values are ignored
    update_height(  # => opens the height-refresh call
        node  # => this insert's subtree root
    )  # => this node's height may have grown after the recursive insert
    balance = balance_factor(node)  # => checks whether THIS node is now unbalanced

    if (  # => opens the LEFT-LEFT case check
        balance > 1  # => the left subtree is at least 2 taller than the right
        and node.left is not None  # => narrows the type: a left-heavy node has a child
        and value < node.left.value  # => left-heavy, straight
    ):  # => LEFT-LEFT
        return rotate_right(node)  # => a single right rotation fixes it
    if (  # => opens the RIGHT-RIGHT case check
        balance < -1  # => the right subtree is at least 2 taller than the left
        and node.right is not None  # => narrows the type: right-heavy has a child
        and value > node.right.value  # => right-heavy, straight
    ):  # => RIGHT-RIGHT
        return rotate_left(node)  # => a single left rotation fixes it
    if (  # => opens the LEFT-RIGHT case check
        balance > 1  # => the left subtree is at least 2 taller than the right
        and node.left is not None  # => narrows the type: a left-heavy node has a child
        and value > node.left.value  # => left-heavy, zig-zag
    ):  # => LEFT-RIGHT
        node.left = rotate_left(node.left)  # => first straighten the left child...
        return rotate_right(node)  # => ...then rotate this node -- a DOUBLE rotation
    if (  # => opens the RIGHT-LEFT case check
        balance < -1  # => the right subtree is at least 2 taller than the left
        and node.right is not None  # => narrows the type: right-heavy has a child
        and value < node.right.value  # => right-heavy, zig-zag
    ):  # => RIGHT-LEFT
        node.right = rotate_right(node.right)  # => first straighten the right child...
        return rotate_left(node)  # => ...then rotate this node -- a DOUBLE rotation
    return node  # => already balanced -- no rotation needed


n = 100  # => 100 sorted keys -- Example 15's exact worst case for a plain BST
root: AVLNode | None = None  # => starts as an empty tree
for k in range(n):  # => inserting in ASCENDING order
    root = avl_insert(root, k)  # => the AVL tree self-balances after every insert

tree_height = height(root)  # => the actual resulting height
log_bound = math.ceil(2 * math.log2(n + 2))  # => a generous O(log n) upper bound
print(tree_height)  # => Output: 7
print(  # => opens the log-bound print call
    log_bound  # => the computed upper bound
)  # => Output: 14 -- confirms tree_height comfortably fits under this bound

# confirms the AVL tree's self-balancing rotations kept height logarithmic
assert tree_height < log_bound  # => confirms O(log n), NOT the O(n) chain of Example 15
assert (  # => opens the height-far-below-n check
    tree_height < n  # => confirms the tree height is nowhere near the input count
)  # => trivially true, but makes the contrast with Example 15 explicit
print("ex-68 OK")  # => Output: ex-68 OK
