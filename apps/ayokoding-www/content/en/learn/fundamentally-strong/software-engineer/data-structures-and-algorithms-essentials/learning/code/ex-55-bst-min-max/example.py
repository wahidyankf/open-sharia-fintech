"""Example 55: BST Minimum and Maximum."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class BSTNode:  # => the same BST node shape as Example 53 (co-11)
    def __init__(self, val: int) -> None:  # => constructor: a leaf with no children yet
        self.val = val  # => the value stored at this node
        self.left: BSTNode | None = None  # => no left child yet
        self.right: BSTNode | None = None  # => no right child yet


def insert(
    root: BSTNode | None, val: int
) -> BSTNode:  # => same insert as Example 53 (co-11)
    if root is None:  # => BASE CASE -- empty slot found
        return BSTNode(val)  # => becomes the new leaf
    if val < root.val:  # => smaller values go left
        root.left = insert(root.left, val)  # => recurse left
    else:  # => equal-or-larger values go right
        root.right = insert(root.right, val)  # => recurse right
    return root  # => the (possibly updated) subtree root


# The minimum is always the LEFTMOST node -- keep walking left until it stops (co-11).
def find_min(node: BSTNode) -> int:  # => an iterative walk, no recursion needed
    while node.left is not None:  # => every left step reaches a smaller value
        node = node.left  # => keep descending left
    return node.val  # => no more left children -- this IS the smallest value


# The maximum is always the RIGHTMOST node -- keep walking right until it stops (co-11).
def find_max(node: BSTNode) -> int:  # => an iterative walk, no recursion needed
    while node.right is not None:  # => every right step reaches a larger value
        node = node.right  # => keep descending right
    return node.val  # => no more right children -- this IS the largest value


root: BSTNode | None = None  # => starts as an empty tree
for value in (5, 2, 8, 1, 3):  # => builds the same BST as Example 53
    root = insert(root, value)  # => grows the BST one value at a time
assert root is not None  # => the loop above always inserts at least one node

smallest = find_min(root)  # => walks left: 5 -> 2 -> 1, stops at 1
largest = find_max(root)  # => walks right: 5 -> 8, stops at 8
print(smallest, largest)  # => Output: 1 8

assert smallest == 1  # => confirms the leftmost node holds the true minimum
assert largest == 8  # => confirms the rightmost node holds the true maximum
print("ex-55 OK")  # => Output: ex-55 OK
