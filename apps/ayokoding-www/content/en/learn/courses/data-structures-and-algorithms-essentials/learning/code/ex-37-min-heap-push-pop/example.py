"""Example 37: Min-Heap with heapq.heappush and heappop."""

# heapq maintains list[0] as the smallest element at all times -- push and pop
# are both O(log n), the cost of re-balancing the binary heap (co-12).
import heapq

heap: list[int] = []  # => an ordinary list, treated as a heap by the heapq functions
for value in (5, 1, 8, 3):  # => pushes in arbitrary order, not sorted order
    heapq.heappush(
        heap, value
    )  # => O(log n): inserts, then bubbles up to restore heap order

popped_order: list[int] = []  # => collects pops to prove ascending order
while heap:  # => drains the heap completely
    popped_order.append(
        heapq.heappop(heap)
    )  # => O(log n): always removes the CURRENT min
print(popped_order)  # => Output: [1, 3, 5, 8]

assert popped_order == [
    1,
    3,
    5,
    8,
]  # => confirms heappop always returns ascending order
print("ex-37 OK")  # => Output: ex-37 OK
