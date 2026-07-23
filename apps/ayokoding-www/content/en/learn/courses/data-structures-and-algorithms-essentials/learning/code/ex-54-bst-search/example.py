"""Example 54: Search a Binary Search Tree."""

from __future__ import (
    annotations,
)  # => lets BSTNode reference "BSTNode" before fully defined


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


# Follows the ONE branch that could contain target -- discards the other half (co-11).
def search(node: BSTNode | None, target: int) -> bool:  # => a plain recursive function
    if node is None:  # => fell off the tree without a match -- not present
        return False  # => target does not exist in this subtree
    if node.val == target:  # => found it
        return True  # => target exists at this node
    if target < node.val:  # => target must be smaller
        return search(node.left, target)  # => target can ONLY be in the left subtree
    return search(node.right, target)  # => target can ONLY be in the right subtree


root: BSTNode | None = None  # => starts as an empty tree
for value in (5, 2, 8, 1, 3):  # => builds the same BST as Example 53
    root = insert(root, value)  # => grows the BST one value at a time

found = search(root, 3)  # => 3 was inserted -- present
missing = search(root, 9)  # => 9 was never inserted -- absent
print(found)  # => Output: True
print(missing)  # => Output: False

assert found is True  # => confirms a present value is found
assert missing is False  # => confirms an absent value is correctly reported missing
print("ex-54 OK")  # => Output: ex-54 OK
