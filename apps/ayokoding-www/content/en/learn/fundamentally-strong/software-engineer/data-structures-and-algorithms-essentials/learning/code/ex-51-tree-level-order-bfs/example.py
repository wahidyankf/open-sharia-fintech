"""Example 51: Level-Order (BFS) Traversal, Grouped by Level."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below
from collections import (
    deque,
)  # => imports the stdlib double-ended queue used as the BFS frontier


class TreeNode:  # => the same binary-tree node shape as Example 48 (co-10)
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ) -> None:  # => constructor: stores the value plus both optional children
        self.val = val  # => the value stored at this node
        self.left = left  # => reference to the left child, or None
        self.right = right  # => reference to the right child, or None


# Breadth-first traversal, one inner list PER DEPTH LEVEL -- a deque as the
# queue gives O(1) popleft, unlike list.pop(0)'s O(n) (co-10, co-06).
def level_order(
    root: TreeNode | None,
) -> list[list[int]]:  # => a queue-driven traversal
    if root is None:  # => an empty tree has zero levels
        return []  # => nothing to traverse
    levels: list[list[int]] = []  # => one entry per depth level, in top-to-bottom order
    queue: deque[TreeNode] = deque([root])  # => FIFO queue seeded with just the root
    while queue:  # => continues until every node has been visited
        level_size = len(
            queue
        )  # => freezes "how many nodes are AT this level right now"
        current_level: list[int] = []  # => collects just this level's values
        for _ in range(level_size):  # => processes exactly this level, not the next one
            node = queue.popleft()  # => O(1): dequeue the next node at this level
            current_level.append(node.val)  # => records this node's value
            if node.left:  # => a left child exists
                queue.append(node.left)  # => enqueue it for the NEXT level
            if node.right:  # => a right child exists
                queue.append(node.right)  # => enqueue it for the NEXT level
        levels.append(current_level)  # => one finished level, added to the result
    return levels  # => the full list-of-lists, one entry per depth


#        4
#       / \
#      2   6
#     / \
#    1   3
root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(6))
levels = level_order(root)  # => groups nodes by depth: [4], [2,6], [1,3]
print(levels)  # => Output: [[4], [2, 6], [1, 3]]

assert levels == [
    [4],
    [2, 6],
    [1, 3],
]  # => confirms both the grouping and per-level order
print("ex-51 OK")  # => Output: ex-51 OK
