"""Example 30: Find the Middle Node with Slow/Fast Pointers."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class Node:  # => the standard singly-linked node shape (co-07)
    def __init__(self, val: int, next: Node | None = None) -> None:  # => constructor
        self.val = val  # => the value stored at this node
        self.next = next  # => pointer to the next node, or None at the tail


# Advances slow by 1 and fast by 2 each step -- when fast hits the end, slow is at
# the middle -- one traversal, no length pre-count needed (co-07, co-20).
def middle_value(head: Node | None) -> int:  # => a two-pointer traversal
    slow = head  # => the "tortoise" -- moves one node per step
    fast = head  # => the "hare" -- moves two nodes per step
    while fast is not None and fast.next is not None:  # => stop when fast runs out
        assert (
            slow is not None
        )  # => invariant: slow never runs past fast, so it's always live here
        slow = slow.next  # => tortoise: +1 node
        fast = fast.next.next  # => hare: +2 nodes -- reaches the end twice as fast
    assert slow is not None  # => the list is non-empty in this example
    return slow.val  # => when fast finishes, slow sits exactly at the middle


odd_list = Node(1, Node(2, Node(3, Node(4, Node(5)))))  # => 5 nodes: middle is 3
middle = middle_value(odd_list)  # => slow lands on the node holding 3
print(middle)  # => Output: 3

assert middle == 3  # => confirms the two-pointer walk found the true middle
print("ex-30 OK")  # => Output: ex-30 OK
