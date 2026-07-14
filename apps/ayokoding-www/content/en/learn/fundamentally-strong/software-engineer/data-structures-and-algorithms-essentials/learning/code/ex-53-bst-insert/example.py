"""Example 53: Insert into a Binary Search Tree."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class BSTNode:  # => an ordered binary tree: left < node < right, always (co-11)
    def __init__(self, val: int) -> None:  # => constructor: a leaf with no children yet
        self.val = val  # => the value stored at this node
        self.left: BSTNode | None = None  # => no left child yet
        self.right: BSTNode | None = None  # => no right child yet


# Descends left/right by comparison until an empty slot is found -- average O(log n) (co-11).
def insert(root: BSTNode | None, val: int) -> BSTNode:  # => a plain recursive function
    if root is None:  # => BASE CASE -- found the empty slot; this becomes a new leaf
        return BSTNode(val)  # => the newly created leaf becomes this subtree's root
    if val < root.val:  # => smaller values always go left
        root.left = insert(root.left, val)  # => recurse into the left subtree
    else:  # => equal-or-larger values always go right
        root.right = insert(root.right, val)  # => recurse into the right subtree
    return root  # => unchanged subtree root, now with the new value inserted somewhere below


# Inorder traversal of a BST always yields values in SORTED order (co-11).
def inorder(node: BSTNode | None) -> list[int]:  # => a plain recursive traversal
    if node is None:  # => BASE CASE -- nothing to visit
        return []  # => no values from this branch
    return inorder(node.left) + [node.val] + inorder(node.right)  # => left, self, right


root: BSTNode | None = None  # => starts as an empty tree
for value in (5, 2, 8, 1, 3):  # => inserts in arbitrary order
    root = insert(root, value)  # => grows the BST one value at a time
sorted_values = inorder(root)  # => the ordering PROPERTY of a BST, made visible
print(sorted_values)  # => Output: [1, 2, 3, 5, 8]

assert sorted_values == [1, 2, 3, 5, 8]  # => confirms inorder yields sorted order
print("ex-53 OK")  # => Output: ex-53 OK
