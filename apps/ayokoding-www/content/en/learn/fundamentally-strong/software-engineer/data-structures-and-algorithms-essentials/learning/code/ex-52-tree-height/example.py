"""Example 52: Compute Tree Height Recursively."""

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


# Height = 1 + the taller of the two child subtrees -- an empty tree has height 0 (co-10, co-17).
def height(node: TreeNode | None) -> int:  # => a plain recursive function
    if node is None:  # => BASE CASE -- no node means no height contributed
        return 0  # => the additive identity for the recursion below
    left_height = height(node.left)  # => RECURSIVE CASE: height of the left subtree
    right_height = height(node.right)  # => RECURSIVE CASE: height of the right subtree
    return 1 + max(left_height, right_height)  # => this node + whichever side is taller


#        4
#       / \
#      2   6
#     / \
#    1   3
root = TreeNode(
    4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6)
)  # => 3 levels deep
tree_height = height(root)  # => 4 -> 2 -> 1 is the longest path, 3 nodes deep
print(tree_height)  # => Output: 3

assert tree_height == 3  # => confirms the height matches the deepest path's node count
assert height(None) == 0  # => confirms an empty tree has height 0
print("ex-52 OK")  # => Output: ex-52 OK
