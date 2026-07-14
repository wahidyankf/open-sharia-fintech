"""Example 70: Lowest Common Ancestor in a BST."""

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


# Uses the BST ordering property: the split point where p and q diverge IS the
# ancestor -- no need to search both subtrees blindly like a plain binary tree (co-11).
def lowest_common_ancestor(
    root: BSTNode, p: int, q: int
) -> int:  # => an iterative walk
    node = root  # => starts the descent at the root
    while (
        True
    ):  # => descends exactly once per level, O(log n) average on a balanced BST
        if (
            p < node.val and q < node.val
        ):  # => both targets are smaller -- LCA is further left
            node = node.left  # => descend into the left subtree
            assert (
                node is not None
            )  # => p and q are both present in the tree, so this can't walk past a leaf
        elif (
            p > node.val and q > node.val
        ):  # => both targets are larger -- LCA is further right
            node = node.right  # => descend into the right subtree
            assert (
                node is not None
            )  # => p and q are both present in the tree, so this can't walk past a leaf
        else:  # => p and q are now on OPPOSITE sides (or one equals node.val) -- found it
            return node.val  # => this node is the lowest common ancestor


root: BSTNode | None = None  # => starts as an empty tree
for value in (6, 2, 8, 0, 4, 7, 9, 3, 5):  # => a moderately deep BST
    root = insert(root, value)
assert root is not None  # => the loop above always inserts at least one node

ancestor = lowest_common_ancestor(
    root, 2, 8
)  # => 2 and 8 split immediately at the root, 6
print(ancestor)  # => Output: 6

assert ancestor == 6  # => confirms the root itself is the LCA of 2 and 8
assert lowest_common_ancestor(root, 0, 4) == 2  # => confirms a deeper LCA also resolves
print("ex-70 OK")  # => Output: ex-70 OK
