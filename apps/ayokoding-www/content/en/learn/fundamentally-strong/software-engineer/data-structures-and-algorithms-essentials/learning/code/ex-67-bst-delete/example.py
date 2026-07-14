"""Example 67: Delete a Node from a BST -- All Three Cases."""

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


# Three cases: leaf (drop it), one child (splice it out), two children
# (replace with the in-order successor -- the smallest node in the right subtree).
def delete(
    root: BSTNode | None, val: int
) -> BSTNode | None:  # => a recursive delete function
    if root is None:  # => value not present -- nothing to delete
        return None  # => an empty subtree stays empty
    if val < root.val:  # => the target is somewhere in the left subtree
        root.left = delete(root.left, val)  # => recurse left, rewire the result back
    elif val > root.val:  # => the target is somewhere in the right subtree
        root.right = delete(root.right, val)  # => recurse right, rewire the result back
    else:  # => root.val == val -- THIS is the node to delete
        if (
            root.left is None
        ):  # => Case: no left child (covers leaf AND one-right-child)
            return (
                root.right
            )  # => splice out root -- promote its right child (or None) up
        if root.right is None:  # => Case: only a left child
            return root.left  # => splice out root -- promote its left child up
        successor = root.right  # => Case: two children -- find the in-order successor
        while successor.left is not None:  # => smallest value in the right subtree
            successor = successor.left  # => keep descending left
        root.val = successor.val  # => copy successor's value into this node
        root.right = delete(
            root.right, successor.val
        )  # => then remove the duplicate successor
    return root  # => the (possibly rewired) subtree root


def inorder(
    node: BSTNode | None,
) -> list[int]:  # => inorder traversal, same shape as before
    if node is None:  # => BASE CASE -- nothing to visit
        return []  # => no values from this branch
    return inorder(node.left) + [node.val] + inorder(node.right)  # => left, self, right


root: BSTNode | None = None  # => starts as an empty tree
for value in (5, 2, 8, 1, 3, 7, 9):  # => builds a small, non-trivial BST
    root = insert(root, value)
root = delete(
    root, 2
)  # => two-children case (2 has children 1 and 3), which recurses into the leaf case
# => (successor 3 has no children of its own) -- 2's slot now holds val 3, left=1, right=None
root = delete(
    root, 3
)  # => one-child case: the node now holding 3 has only a left child (1), no right child
result = inorder(root)  # => must STILL be sorted after both deletes
print(result)  # => Output: [1, 5, 7, 8, 9]

assert (
    result
    == [
        1,
        5,
        7,
        8,
        9,
    ]
)  # => confirms sorted order survives all three delete cases (two-children, leaf, one-child)
assert 2 not in result and 3 not in result  # => confirms both deleted values are gone
print("ex-67 OK")  # => Output: ex-67 OK
