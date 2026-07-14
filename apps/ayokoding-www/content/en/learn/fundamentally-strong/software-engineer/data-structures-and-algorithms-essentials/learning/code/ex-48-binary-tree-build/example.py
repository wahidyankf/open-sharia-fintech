"""Example 48: Build a Binary Tree."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below
from collections import (
    deque,
)  # => imports the stdlib double-ended queue for the BFS below


class TreeNode:  # => a node with up to two children: left and right (co-10, co-22)
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ) -> None:  # => constructor: stores the value plus both optional children
        self.val = val  # => the value stored at this node
        self.left = left  # => reference to the left child, or None
        self.right = right  # => reference to the right child, or None


#        4
#       / \
#      2   6
#     / \
#    1   3
root = TreeNode(
    4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6)
)  # => builds by hand

level_order: list[int] = []  # => collects values level by level, to eyeball the shape
queue: deque[TreeNode] = deque([root])  # => a queue seeded with just the root
while queue:  # => classic BFS: visit, then enqueue children, until the queue is empty
    node = queue.popleft()  # => dequeues the next node to visit, O(1)
    level_order.append(node.val)  # => records this node's value
    if node.left:  # => a left child exists
        queue.append(node.left)  # => enqueues it for a later visit
    if node.right:  # => a right child exists
        queue.append(node.right)  # => enqueues it for a later visit
print(level_order)  # => Output: [4, 2, 6, 1, 3]

assert level_order == [4, 2, 6, 1, 3]  # => confirms the tree's exact level-order shape
print("ex-48 OK")  # => Output: ex-48 OK
