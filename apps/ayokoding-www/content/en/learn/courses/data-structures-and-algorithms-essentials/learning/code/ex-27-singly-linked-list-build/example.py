"""Example 27: Build a Singly Linked List."""

from __future__ import (
    annotations,
)  # => lets Node reference "Node" before it's fully defined


class Node:  # => a node-based sequence: each Node holds one value plus a pointer (co-07, co-22)
    def __init__(self, val: int, next: Node | None = None) -> None:  # => constructor
        self.val = val  # => the value stored at this node
        self.next = next  # => a reference to the NEXT node, or None if this is the tail


# Building the list 1 -> 2 -> 3 by wiring .next pointers from the tail backward.
third = Node(3)  # => tail node: val=3, next=None
second = Node(2, third)  # => middle node: val=2, next points at third
head = Node(1, second)  # => head node: val=1, next points at second -- O(1) insertion

values: list[int] = []  # => collects values while traversing
current: Node | None = head  # => starts traversal at the head
while current is not None:  # => walks the chain until next is None -- O(n) traversal
    values.append(current.val)  # => records this node's value
    current = current.next  # => advances one link forward
print(values)  # => Output: [1, 2, 3]

assert values == [1, 2, 3]  # => confirms traversal visited nodes in link order
print("ex-27 OK")  # => Output: ex-27 OK
