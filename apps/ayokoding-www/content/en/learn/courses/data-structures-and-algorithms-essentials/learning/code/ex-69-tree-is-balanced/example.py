"""Example 69: Check Whether a Binary Tree Is Height-Balanced."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class TreeNode:  # => the same binary-tree node shape as Example 48 (co-10)
    def __init__(
        self,
        val: int,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
        # => three params: the value plus each optional child, defaulting to leaf
    ) -> None:  # => constructor: stores the value plus both optional children
        self.val = val  # => the value stored at this node
        self.left = left  # => reference to the left child, or None
        self.right = right  # => reference to the right child, or None


# Returns height, or -1 as a sentinel the moment ANY subtree is unbalanced --
# stops early instead of recomputing height and balance in two separate passes (co-10, co-17).
def height_if_balanced(
    node: TreeNode | None,
) -> int:  # => a single-pass recursive check
    if node is None:  # => BASE CASE -- an empty subtree is balanced with height 0
        return 0  # => contributes no height and no imbalance
    left_height = height_if_balanced(
        node.left
    )  # => RECURSIVE CASE: check the left subtree first
    if left_height == -1:  # => left subtree already failed
        return -1  # => propagate the failure up
    right_height = height_if_balanced(
        node.right
    )  # => RECURSIVE CASE: check the right subtree
    if right_height == -1:  # => right subtree already failed
        return -1  # => propagate the failure up
    if (
        abs(left_height - right_height) > 1
    ):  # => the balance CONDITION: heights differ by <= 1
        return -1  # => unbalanced at this node -- signal failure upward
    return 1 + max(
        left_height, right_height
    )  # => balanced here -- report the real height


def is_balanced(
    root: TreeNode | None,
) -> bool:  # => a thin wrapper over the sentinel check
    return (
        height_if_balanced(root) != -1
    )  # => -1 anywhere in the tree means "not balanced"


balanced_tree = TreeNode(
    1, TreeNode(2), TreeNode(3)
)  # => both subtrees height 1 -- balanced
unbalanced_tree = TreeNode(
    1, TreeNode(2, TreeNode(3))
)  # => left is deeper by 2 -- unbalanced
result_balanced = is_balanced(balanced_tree)  # => checks the shallow, even tree
result_unbalanced = is_balanced(unbalanced_tree)  # => checks the lopsided tree
print(result_balanced)  # => Output: True
print(result_unbalanced)  # => Output: False

assert result_balanced is True  # => confirms a shallow, even tree is reported balanced
assert result_unbalanced is False  # => confirms a lopsided tree is reported unbalanced
print("ex-69 OK")  # => Output: ex-69 OK
