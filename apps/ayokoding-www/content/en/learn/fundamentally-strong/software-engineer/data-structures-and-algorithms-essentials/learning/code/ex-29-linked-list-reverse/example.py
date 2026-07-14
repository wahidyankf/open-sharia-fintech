"""Example 29: Reverse a Singly Linked List Iteratively."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class Node:  # => the standard singly-linked node shape (co-07)
    def __init__(self, val: int, next: Node | None = None) -> None:  # => constructor
        self.val = val  # => the value stored at this node
        self.next = next  # => pointer to the next node, or None at the tail


# Flips every .next pointer to point backward -- one O(n) pass, O(1) extra space (co-07).
def reverse(head: Node | None) -> Node | None:  # => rewires the chain in place
    previous: Node | None = None  # => will become the new head once the loop finishes
    current = head  # => the node currently being rewired
    while current is not None:  # => walks forward through the ORIGINAL chain
        next_node = current.next  # => save the forward link BEFORE overwriting it
        current.next = previous  # => rewire: point this node back at the previous one
        previous = current  # => advance "previous" to this now-rewired node
        current = next_node  # => advance "current" using the saved forward link
    return previous  # => previous ends up at the old TAIL -- the new head


# Collects node values in link order for easy comparison.
def to_list(head: Node | None) -> list[int]:  # => a plain traversal helper
    values: list[int] = []  # => accumulates values as the chain is walked
    node = head  # => starts traversal at head
    while node is not None:  # => stops once the tail's next is None
        values.append(node.val)  # => records this node's value
        node = node.next  # => advances one link forward
    return values  # => the values in link order


original = Node(1, Node(2, Node(3, Node(4))))  # => 1 -> 2 -> 3 -> 4
reversed_head = reverse(
    original
)  # => rewires in place -- returns the new head (old node 4)
print(to_list(reversed_head))  # => Output: [4, 3, 2, 1]

assert to_list(reversed_head) == [4, 3, 2, 1]  # => confirms the chain is fully reversed
print("ex-29 OK")  # => Output: ex-29 OK
