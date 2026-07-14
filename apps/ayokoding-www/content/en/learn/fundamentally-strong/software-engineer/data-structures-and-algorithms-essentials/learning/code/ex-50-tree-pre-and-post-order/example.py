"""Example 50: Preorder and Postorder Traversals."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class TreeNode:  # => the same binary-tree node shape as Example 48 (co-10)
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ) -> None:  # => constructor: stores the value plus both optional children
        self.val = val  # => the value stored at this node
        self.left = left  # => reference to the left child, or None
        self.right = right  # => reference to the right child, or None


# Visits self, THEN left, THEN right (co-10, co-17).
def preorder(node: TreeNode | None) -> list[int]:  # => a plain recursive traversal
    if node is None:  # => BASE CASE -- nothing to visit
        return []  # => no values from this branch
    return (
        [node.val] + preorder(node.left) + preorder(node.right)
    )  # => self, left, right


# Visits left, THEN right, THEN self -- self is visited LAST (co-10, co-17).
def postorder(node: TreeNode | None) -> list[int]:  # => a plain recursive traversal
    if node is None:  # => BASE CASE -- nothing to visit
        return []  # => no values from this branch
    return (
        postorder(node.left) + postorder(node.right) + [node.val]
    )  # => left, right, self


#        4
#       / \
#      2   6
#     / \
#    1   3
root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6))
pre = preorder(root)  # => root first: 4, 2, 1, 3, 6
post = postorder(root)  # => root last: 1, 3, 2, 6, 4
print(pre)  # => Output: [4, 2, 1, 3, 6]
print(post)  # => Output: [1, 3, 2, 6, 4]

assert pre == [
    4,
    2,
    1,
    3,
    6,
]  # => confirms preorder visits the root before its children
assert post == [
    1,
    3,
    2,
    6,
    4,
]  # => confirms postorder visits the root after its children
print("ex-50 OK")  # => Output: ex-50 OK
