"""Example 42: Merge Two Sorted Lists with heapq.merge."""

# heapq.merge streams both inputs through a small heap, producing sorted output
# without concatenating and re-sorting -- O(n) for two already-sorted inputs (co-12, co-15).
import heapq

left: list[int] = [1, 4, 7]  # => already sorted
right: list[int] = [2, 3, 8]  # => already sorted
merged = list(
    heapq.merge(left, right)
)  # => lazily interleaves both inputs in sorted order
print(merged)  # => Output: [1, 2, 3, 4, 7, 8]

assert merged == [1, 2, 3, 4, 7, 8]  # => confirms full interleaved sorted order
assert merged == sorted(
    left + right
)  # => cross-checks against a plain sort of the union
print("ex-42 OK")  # => Output: ex-42 OK
