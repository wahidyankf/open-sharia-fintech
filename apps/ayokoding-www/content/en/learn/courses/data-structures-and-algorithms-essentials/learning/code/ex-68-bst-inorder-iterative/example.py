"""Example 68: Iterative Inorder Traversal with an Explicit Stack."""

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


# The familiar recursive version, for comparison (co-11, co-17).
def inorder_recursive(
    node: BSTNode | None,
) -> list[int]:  # => call-stack-based traversal
    if node is None:  # => BASE CASE -- nothing to visit
        return []  # => no values from this branch
    return inorder_recursive(node.left) + [node.val] + inorder_recursive(node.right)


# Same traversal, but an explicit list-as-stack replaces the call stack (co-11, co-04, co-18).
def inorder_iterative(
    root: BSTNode | None,
) -> list[int]:  # => manual-stack-based traversal
    result: list[
        int
    ] = []  # => collects visited values, same order as the recursive version
    stack: list[
        BSTNode
    ] = []  # => a manual stack -- append() pushes, pop() pops (co-04)
    node = root  # => the node currently being descended into
    while (
        stack or node is not None
    ):  # => continue while there's work on the stack OR below us
        while (
            node is not None
        ):  # => walk all the way left, pushing each node along the way
            stack.append(node)  # => remembers this ancestor for later
            node = node.left  # => keeps descending left
        node = stack.pop()  # => backtrack to the deepest unvisited ancestor
        result.append(
            node.val
        )  # => visit it NOW -- this is the "self" step of left-self-right
        node = node.right  # => then descend into its right subtree next
    return result  # => the full inorder-visited values, iteratively collected


root: BSTNode | None = None  # => starts as an empty tree
for value in (5, 2, 8, 1, 3, 7, 9):  # => builds the same fixture as Example 67
    root = insert(
        root, value
    )  # => builds the same shape as Example 67, one insert per value

recursive_order = inorder_recursive(root)  # => the call-stack-based traversal
iterative_order = inorder_iterative(root)  # => the explicit-stack traversal
print(recursive_order)  # => Output: [1, 2, 3, 5, 7, 8, 9]
print(iterative_order)  # => Output: [1, 2, 3, 5, 7, 8, 9]

assert iterative_order == recursive_order  # => confirms both traversals agree exactly
print("ex-68 OK")  # => Output: ex-68 OK
