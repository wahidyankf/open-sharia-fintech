"""Example 69: Red-Black Tree -- Verifying Both Core Invariants After Every Insert."""

# A red-black tree (co-12) balances via COLOR, not strict height matching:
# (1) no red node has a red child ("no red-red"), and (2) every root-to-leaf
# path has the SAME count of black nodes ("equal black-heights"). Together
# these two rules bound height at O(log n), enforced by rotations + recolors.
from __future__ import annotations  # => allows RBNode to reference itself in type hints

from enum import Enum, auto  # => Color is an Enum, not a bare string, for type safety


class Color(Enum):  # => the two colors every red-black node can have
    RED = auto()  # => a freshly inserted node always starts RED
    BLACK = auto()  # => the root, and every "missing" leaf, count as BLACK


class RBNode:  # => a BST node with a color and an explicit parent pointer
    def __init__(self, value: int) -> None:  # => a fresh node, always inserted RED
        self.value = value  # => this node's key
        self.color = Color.RED  # => new nodes are always inserted RED
        self.left: RBNode | None = None  # => no left child yet
        self.right: RBNode | None = None  # => no right child yet
        self.parent: RBNode | None = None  # => no parent yet -- set by the caller


class RedBlackTree:  # => wraps the root pointer and the insert/fixup/rotation logic
    def __init__(self) -> None:  # => an empty tree
        self.root: RBNode | None = None  # => no nodes yet

    def insert(self, value: int) -> None:  # => standard BST insert, then FIXUP
        node = RBNode(value)  # => the new node, colored RED by default
        parent: RBNode | None = None  # => tracks the eventual parent during descent
        current = self.root  # => starts the descent from the root
        while current is not None:  # => standard BST descent to find node's spot
            parent = current  # => remembers the last node visited
            if value < current.value:  # => belongs in the LEFT subtree
                current = current.left  # => descends left
            elif value > current.value:  # => belongs in the RIGHT subtree
                current = current.right  # => descends right
            else:  # => value already exists in the tree
                return  # => duplicate value -- ignored
        node.parent = parent  # => attaches the new node under its found parent
        if parent is None:  # => the tree was empty -- node becomes the root
            self.root = node  # => the new node is now the whole tree
        elif value < parent.value:  # => attaches as the LEFT child
            parent.left = node  # => links the new node in
        else:  # => attaches as the RIGHT child
            parent.right = node  # => links the new node in
        self._fixup(node)  # => restores the two invariants, possibly via rotations

    def _fixup(self, node: RBNode) -> None:  # => the classic CLRS red-black fixup loop
        while (  # => opens the red-red-violation loop condition
            node.parent is not None  # => stops once node reaches the (black) root
            and node.parent.color == Color.RED  # => parent exists and is RED
        ):  # => a red-red violation exists between node and its parent
            grandparent = node.parent.parent  # => needed to identify node's UNCLE
            assert (  # => opens the non-root-parent sanity check
                grandparent is not None  # => guaranteed by the loop's own condition
            )  # => a red parent is never the root (root is black)
            if node.parent == grandparent.left:  # => parent is a LEFT child
                uncle = grandparent.right  # => the OTHER child of the grandparent
                if (  # => opens the red-uncle check
                    uncle is not None  # => a genuine sibling subtree exists
                    and uncle.color == Color.RED  # => uncle exists and is RED
                ):  # => RED uncle: recolor
                    node.parent.color = Color.BLACK  # => pushes the red-red fix upward
                    uncle.color = (  # => opens the uncle recolor
                        Color.BLACK  # => the uncle turns black
                    )  # => keeps black-height balanced on both sides
                    grandparent.color = (  # => opens the grandparent recolor
                        Color.RED  # => grandparent turns red, absorbing the fix
                    )  # => grandparent may now violate red-red itself
                    node = grandparent  # => the violation may have moved UP -- keep looping
                else:  # => BLACK (or absent) uncle: rotation(s) needed
                    if (  # => opens the zig-zag-shape check
                        node
                        == node.parent.right  # => node is the RIGHT child of a LEFT-child parent
                    ):  # => a "zig-zag" shape -- straighten first
                        node = (  # => opens the pre-rotation re-anchor
                            node.parent  # => the parent becomes the new pivot node
                        )  # => re-anchors node at the parent for the pre-rotation
                        self._rotate_left(  # => opens the zig-zag-straightening rotation
                            node  # => rotates around the re-anchored node
                        )  # => converts zig-zag into a straight zig-zig
                    assert node.parent is not None  # => the fixup loop guarantees this
                    node.parent.color = Color.BLACK  # => recolors after the rotation
                    grandparent.color = (  # => opens the grandparent recolor
                        Color.RED  # => grandparent turns red before dropping down
                    )  # => grandparent drops down and turns red
                    self._rotate_right(  # => opens the final balance-restoring rotation
                        grandparent  # => rotates around the grandparent
                    )  # => the final rotation restores balance
            else:  # => the mirror image: parent is a RIGHT child
                uncle = grandparent.left  # => the OTHER child of the grandparent
                if (  # => opens the mirrored red-uncle check
                    uncle is not None  # => a genuine sibling subtree exists
                    and uncle.color == Color.RED  # => uncle exists and is RED
                ):  # => RED uncle: recolor case
                    node.parent.color = Color.BLACK  # => pushes the red-red fix upward
                    uncle.color = (  # => opens the uncle recolor
                        Color.BLACK  # => the uncle turns black
                    )  # => keeps black-height balanced on both sides
                    grandparent.color = (  # => opens the grandparent recolor
                        Color.RED  # => grandparent turns red, absorbing the fix
                    )  # => grandparent may now violate red-red itself
                    node = grandparent  # => the violation may have moved UP -- keep looping
                else:  # => BLACK (or absent) uncle: rotation(s) needed
                    if (  # => opens the mirrored zig-zag-shape check
                        node == node.parent.left  # => node is the LEFT child here
                    ):  # => a "zig-zag" shape -- straighten first case
                        node = (  # => opens the pre-rotation re-anchor
                            node.parent  # => the parent becomes the new pivot node
                        )  # => re-anchors node at the parent for the pre-rotation
                        self._rotate_right(  # => opens the zig-zag-straightening rotation
                            node  # => rotates around the re-anchored node
                        )  # => converts zig-zag into a straight zig-zig
                    assert node.parent is not None  # => the fixup loop guarantees this
                    node.parent.color = Color.BLACK  # => recolors after the rotation
                    grandparent.color = (  # => opens the grandparent recolor
                        Color.RED  # => grandparent turns red before dropping down
                    )  # => grandparent drops down and turns red
                    self._rotate_left(  # => opens the final balance-restoring rotation
                        grandparent  # => rotates around the grandparent
                    )  # => the final rotation restores balance
        assert self.root is not None  # => the tree is non-empty after any insert
        self.root.color = Color.BLACK  # => THE INVARIANT: the root is always black

    def _rotate_left(  # => standard BST left rotation, plus parent-pointer upkeep
        self,  # => the tree instance, so self.root can be updated if needed
        x: RBNode,  # => the node rotating down; its right child rises
    ) -> None:  # => standard BST left rotation, plus parent links
        y = x.right  # => y is guaranteed non-None whenever this is called
        assert y is not None  # => only called when x has a right child
        x.right = y.left  # => y's left subtree becomes x's new right subtree
        if y.left is not None:  # => re-parents that subtree, if it exists
            y.left.parent = x  # => keeps the parent pointer consistent
        y.parent = x.parent  # => y takes x's old place in the tree
        if x.parent is None:  # => x WAS the root
            self.root = y  # => y becomes the new root
        elif x == x.parent.left:  # => x was a LEFT child
            x.parent.left = y  # => y takes x's place as the left child
        else:  # => x was a RIGHT child
            x.parent.right = y  # => y takes x's place as the right child
        y.left = x  # => x becomes y's left child -- y rises to take x's old position
        x.parent = y  # => completes the parent-pointer swap

    def _rotate_right(self, x: RBNode) -> None:  # => the mirror image of _rotate_left
        y = x.left  # => y is guaranteed non-None whenever this is called
        assert y is not None  # => only called when x has a left child
        x.left = y.right  # => y's right subtree becomes x's new left subtree
        if y.right is not None:  # => re-parents that subtree, if it exists
            y.right.parent = x  # => keeps the parent pointer consistent
        y.parent = x.parent  # => y takes x's old place in the tree
        if x.parent is None:  # => x WAS the root
            self.root = y  # => y becomes the new root
        elif x == x.parent.right:  # => x was a RIGHT child
            x.parent.right = y  # => y takes x's place as the right child
        else:  # => x was a LEFT child
            x.parent.left = y  # => y takes x's place as the left child
        y.right = x  # => x becomes y's right child -- y rises to take x's old position
        x.parent = y  # => completes the parent-pointer swap


def no_red_red_violation(node: RBNode | None) -> bool:  # => INVARIANT 1 checker
    if node is None:  # => an absent child counts as black -- no violation possible
        return True  # => nothing to violate at an empty leaf
    if node.color == Color.RED:  # => a red node's children must BOTH be non-red
        if (  # => opens the left-child red-red check
            node.left is not None  # => a genuine left child exists
            and node.left.color == Color.RED  # => and it's also RED -- a violation
        ):  # => red-red on the left
            return False  # => a genuine violation
        if (  # => opens the right-child red-red check
            node.right is not None  # => a genuine right child exists
            and node.right.color == Color.RED  # => and it's also RED -- a violation
        ):  # => red-red on the right
            return False  # => a genuine violation
    return no_red_red_violation(  # => opens the left-subtree recursive check
        node.left  # => recursively checks the left subtree
    ) and no_red_red_violation(  # => checks the left subtree
        node.right  # => and the right subtree
    )  # => recursively checks the whole tree


def black_height(  # => counts BLACK nodes on any root-to-leaf path, or -1 if unequal
    node: RBNode | None,  # => the subtree root to measure
) -> int:  # => INVARIANT 2 checker: -1 means violated
    if (  # => opens the empty-leaf base case check
        node is None  # => reached past a real node -- the implicit black leaf
    ):  # => an absent leaf contributes exactly 1 to any path's black count
        return 1  # => the base case for every root-to-leaf path
    left = black_height(node.left)  # => recursively checks the left subtree first
    right = black_height(node.right)  # => then the right subtree
    if left == -1 or right == -1 or left != right:  # => already broken, or MISMATCHED
        return -1  # => propagates the violation upward
    return left + (  # => opens the this-node's-own-color tally
        1 if node.color == Color.BLACK else 0  # => BLACK nodes count, RED nodes don't
    )  # => tallies this node if BLACK


tree = RedBlackTree()  # => an empty red-black tree
for v in range(200):  # => 200 ASCENDING inserts -- a plain BST's absolute worst case
    tree.insert(v)  # => rotations + recolors keep it balanced throughout

print(no_red_red_violation(tree.root))  # => Output: True
print(black_height(tree.root) != -1)  # => Output: True
assert tree.root is not None  # => narrows the type for the color check below
print(tree.root.color == Color.BLACK)  # => Output: True

assert no_red_red_violation(  # => opens the invariant-1 assertion
    tree.root  # => the fully-built 200-node tree
)  # => confirms invariant 1 holds after 200 inserts
assert (  # => opens the invariant-2 assertion
    black_height(tree.root) != -1  # => a non-negative-one result means it's balanced
)  # => confirms invariant 2 (equal black-heights) holds
assert tree.root.color == Color.BLACK  # => confirms the root invariant holds
print("ex-69 OK")  # => Output: ex-69 OK
