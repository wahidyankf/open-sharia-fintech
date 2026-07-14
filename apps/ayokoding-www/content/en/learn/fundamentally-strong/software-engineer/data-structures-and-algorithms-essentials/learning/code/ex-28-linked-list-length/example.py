"""Example 28: Linked List Length by Traversal."""

from __future__ import annotations  # => lets Node reference "Node" before fully defined


class Node:  # => the same node shape as Example 27 (co-07)
    def __init__(self, val: int, next: Node | None = None) -> None:  # => constructor
        self.val = val  # => this node's stored value
        self.next = next  # => pointer to the next node, or None at the tail


# Counts nodes by walking the chain -- O(n), no random-access shortcut exists (co-07).
def length(head: Node | None) -> int:  # => a plain traversal function
    count = 0  # => starts at zero nodes counted
    current = head  # => begins traversal at the head
    while current is not None:  # => stops once we fall off the tail (next is None)
        count += 1  # => counts this node
        current = current.next  # => advances to the next link
    return count  # => the total number of nodes visited


head = Node(1, Node(2, Node(3, Node(4))))  # => builds a 4-node chain: 1->2->3->4
node_count = length(head)  # => walks all 4 nodes to count them
print(node_count)  # => Output: 4

assert node_count == 4  # => confirms the traversal counted every node exactly once
assert length(None) == 0  # => confirms an empty list (no head) has length 0
print("ex-28 OK")  # => Output: ex-28 OK
