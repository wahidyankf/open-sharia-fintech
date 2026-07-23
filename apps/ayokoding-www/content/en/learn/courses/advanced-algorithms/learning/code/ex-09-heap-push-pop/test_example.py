"""Example 9: pytest verification for heapq Push and Pop."""

import heapq


def test_heap_drains_in_ascending_order_regardless_of_push_order() -> None:
    heap: list[int] = []
    for value in [40, 10, 30, 20, 50]:  # => unsorted push order
        heapq.heappush(heap, value)
    drained = [heapq.heappop(heap) for _ in range(len(heap))]  # => drains to empty
    assert drained == [10, 20, 30, 40, 50]  # => always emerges smallest-first


def test_heap_top_is_always_current_minimum() -> None:
    heap: list[int] = [7, 2, 9]
    heapq.heapify(heap)  # => O(n): rearranges an existing list into heap order
    assert heap[0] == 2  # => the minimum is always readable at index 0


# => Run: pytest -- Output: 2 passed
