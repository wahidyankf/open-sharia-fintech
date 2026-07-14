"""Example 49: Recursive Inorder Traversal."""

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


# Visits left, THEN self, THEN right -- depth-first, recursive (co-10, co-17).
def inorder(node: TreeNode | None) -> list[int]:  # => a plain recursive traversal
    if node is None:  # => BASE CASE -- an empty subtree contributes nothing
        return []  # => no values from this branch
    return inorder(node.left) + [node.val] + inorder(node.right)  # => left, self, right


#        4
#       / \
#      2   6
#     / \
#    1   3
root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6))
values = inorder(root)  # => visits 1, 2, 3, 4, 6 -- left subtree, root, right subtree
print(values)  # => Output: [1, 2, 3, 4, 6]

assert values == [1, 2, 3, 4, 6]  # => confirms the exact left-root-right visit order
print("ex-49 OK")  # => Output: ex-49 OK
