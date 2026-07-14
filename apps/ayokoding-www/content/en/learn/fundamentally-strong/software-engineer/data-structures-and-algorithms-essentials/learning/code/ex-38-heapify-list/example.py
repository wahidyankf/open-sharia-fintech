"""Example 38: heapq.heapify -- Turn a List into a Heap In Place."""

# heapify rearranges an EXISTING list into heap order in O(n) -- faster than
# pushing every element one at a time, which would cost O(n log n) (co-12).
import heapq

values: list[int] = [9, 4, 7, 1, 3]  # => an unordered list, not yet heap-shaped
heapq.heapify(values)  # => O(n): rearranges values in place into a valid min-heap
print(values[0])  # => Output: 1 (the minimum -- always at index 0 after heapify)

assert values[0] == min([9, 4, 7, 1, 3])  # => confirms heap[0] equals the true minimum
assert heapq.heappop(values) == 1  # => confirms popping still yields the minimum first
print("ex-38 OK")  # => Output: ex-38 OK
