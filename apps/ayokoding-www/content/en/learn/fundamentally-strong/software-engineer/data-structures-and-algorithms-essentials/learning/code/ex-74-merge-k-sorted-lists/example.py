"""Example 74: Merge k Sorted Linked Lists with a Heap."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below
import heapq  # => imports the stdlib binary-heap functions


class Node:  # => the standard singly-linked node shape (co-07)
    def __init__(self, val: int, next: Node | None = None) -> None:  # => constructor
        self.val = val  # => the value stored at this node
        self.next = next  # => pointer to the next node, or None at the tail


# Seeds a heap with each list's current head; always takes the global minimum next.
# A heap turns "compare k candidates every step" into an O(log k) operation
# instead of an O(k) linear scan across all k list heads each time (co-12, co-07).
def merge_k_lists(
    heads: list[Node | None],
) -> Node | None:  # => a heap-driven k-way merge
    heap: list[
        tuple[int, int, Node]
    ] = []  # => (value, tie_breaker, node) -- see note below
    for i, head in enumerate(
        heads
    ):  # => tie_breaker=i avoids comparing Node objects directly
        if head is not None:  # => skip any list that starts out empty
            heapq.heappush(
                heap, (head.val, i, head)
            )  # => seeds with each list's first node

    dummy = Node(0)  # => a throwaway head so the result never needs a None-check
    tail = dummy  # => tail always points at the last node appended so far
    while heap:  # => O((n) log k): n total nodes, each heap op costs log k
        _val, i, node = heapq.heappop(
            heap
        )  # => the smallest value among all k frontiers
        tail.next = node  # => appends the global minimum to the merged result
        tail = tail.next  # => advances the tail pointer to the newly appended node
        if node.next is not None:  # => that list still has more nodes
            heapq.heappush(heap, (node.next.val, i, node.next))  # => push its new head
    return dummy.next  # => skips the dummy sentinel, returns the real merged head


def to_list(head: Node | None) -> list[int]:  # => a plain traversal helper
    values: list[int] = []  # => accumulates values as the chain is walked
    node = head  # => starts traversal at head
    while node is not None:  # => stops once the tail's next is None
        values.append(node.val)  # => records this node's value
        node = node.next  # => advances one link forward
    return values  # => the values in link order


list_a = Node(1, Node(4, Node(5)))  # => 1 -> 4 -> 5
list_b = Node(1, Node(3, Node(4)))  # => 1 -> 3 -> 4
list_c = Node(2, Node(6))  # => 2 -> 6
merged_head = merge_k_lists(
    [list_a, list_b, list_c]
)  # => interleaves all three by value
result = to_list(merged_head)  # => flattens the merged chain into a plain list
print(result)  # => Output: [1, 1, 2, 3, 4, 4, 5, 6]

assert result == [
    1,
    1,
    2,
    3,
    4,
    4,
    5,
    6,
]  # => confirms full sorted interleave of all 3 lists
assert result == sorted(
    result
)  # => cross-checks that the merged output is truly sorted
print("ex-74 OK")  # => Output: ex-74 OK
