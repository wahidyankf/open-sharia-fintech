"""Example 69: Red-Black Tree -- Verifying Both Core Invariants After Every Insert."""

# A red-black tree (co-12) balances via COLOR, not strict height matching:
# (1) no red node has a red child ("no red-red"), and (2) every root-to-leaf
# path has the SAME count of black nodes ("equal black-heights"). Together
# these two rules bound height at O(log n), enforced by rotations + recolors.
from __future__ import annotations

from enum import Enum, auto


class Color(Enum):
    RED = auto()  # => a freshly inserted node always starts RED
    BLACK = auto()  # => the root, and every "missing" leaf, count as BLACK


class RBNode:  # => a BST node with a color and an explicit parent pointer
    def __init__(self, value: int) -> None:
        self.value = value
        self.color = Color.RED  # => new nodes are always inserted RED
        self.left: RBNode | None = None
        self.right: RBNode | None = None
        self.parent: RBNode | None = None


class RedBlackTree:
    def __init__(self) -> None:
        self.root: RBNode | None = None

    def insert(self, value: int) -> None:  # => standard BST insert, then FIXUP
        node = RBNode(value)
        parent: RBNode | None = None
        current = self.root
        while current is not None:  # => standard BST descent to find node's spot
            parent = current
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return  # => duplicate value -- ignored
        node.parent = parent
        if parent is None:  # => the tree was empty -- node becomes the root
            self.root = node
        elif value < parent.value:
            parent.left = node
        else:
            parent.right = node
        self._fixup(node)  # => restores the two invariants, possibly via rotations

    def _fixup(self, node: RBNode) -> None:  # => the classic CLRS red-black fixup loop
        while (
            node.parent is not None and node.parent.color == Color.RED
        ):  # => a red-red violation exists between node and its parent
            grandparent = node.parent.parent
            assert (
                grandparent is not None
            )  # => a red parent is never the root (root is black)
            if node.parent == grandparent.left:  # => parent is a LEFT child
                uncle = grandparent.right
                if (
                    uncle is not None and uncle.color == Color.RED
                ):  # => RED uncle: recolor
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    node = grandparent  # => the violation may have moved UP -- keep looping
                else:  # => BLACK (or absent) uncle: rotation(s) needed
                    if (
                        node == node.parent.right
                    ):  # => a "zig-zag" shape -- straighten first
                        node = node.parent
                        self._rotate_left(node)
                    assert node.parent is not None  # => the fixup loop guarantees this
                    node.parent.color = Color.BLACK  # => recolors after the rotation
                    grandparent.color = Color.RED
                    self._rotate_right(grandparent)
            else:  # => the mirror image: parent is a RIGHT child
                uncle = grandparent.left
                if uncle is not None and uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    grandparent.color = Color.RED
                    node = grandparent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    assert node.parent is not None  # => the fixup loop guarantees this
                    node.parent.color = Color.BLACK
                    grandparent.color = Color.RED
                    self._rotate_left(grandparent)
        assert self.root is not None  # => the tree is non-empty after any insert
        self.root.color = Color.BLACK  # => THE INVARIANT: the root is always black

    def _rotate_left(self, x: RBNode) -> None:
        y = x.right
        assert y is not None  # => only called when x has a right child
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x: RBNode) -> None:
        y = x.left
        assert y is not None  # => only called when x has a left child
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


def no_red_red_violation(node: RBNode | None) -> bool:  # => INVARIANT 1 checker
    if node is None:  # => an absent child counts as black -- no violation possible
        return True
    if node.color == Color.RED:  # => a red node's children must BOTH be non-red
        if node.left is not None and node.left.color == Color.RED:
            return False
        if node.right is not None and node.right.color == Color.RED:
            return False
    return no_red_red_violation(node.left) and no_red_red_violation(
        node.right
    )  # => recursively checks the whole tree


def black_height(
    node: RBNode | None,
) -> int:  # => INVARIANT 2 checker: -1 means violated
    if (
        node is None
    ):  # => an absent leaf contributes exactly 1 to any path's black count
        return 1
    left = black_height(node.left)  # => recursively checks the left subtree first
    right = black_height(node.right)  # => then the right subtree
    if left == -1 or right == -1 or left != right:  # => already broken, or MISMATCHED
        return -1  # => propagates the violation upward
    return left + (
        1 if node.color == Color.BLACK else 0
    )  # => tallies this node if BLACK


tree = RedBlackTree()  # => an empty red-black tree
for v in range(200):  # => 200 ASCENDING inserts -- a plain BST's absolute worst case
    tree.insert(v)  # => rotations + recolors keep it balanced throughout

print(no_red_red_violation(tree.root))  # => Output: True
print(black_height(tree.root) != -1)  # => Output: True
assert tree.root is not None  # => narrows the type for the color check below
print(tree.root.color == Color.BLACK)  # => Output: True

assert no_red_red_violation(
    tree.root
)  # => confirms invariant 1 holds after 200 inserts
assert (
    black_height(tree.root) != -1
)  # => confirms invariant 2 (equal black-heights) holds
assert tree.root.color == Color.BLACK  # => confirms the root invariant holds
print("ex-69 OK")  # => Output: ex-69 OK
