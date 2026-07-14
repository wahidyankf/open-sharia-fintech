"""Example 39: Top-K Largest with heapq.nlargest."""

# heapq.nlargest keeps only a size-k heap while scanning, O(n log k) --
# cheaper than sorted(values)[-k:], which pays O(n log n) for the WHOLE list (co-12).
import heapq

values: list[int] = [5, 1, 9, 3, 7, 2]  # => 6 values, only the top 3 are wanted
top_three = heapq.nlargest(3, values)  # => returns the 3 largest, in descending order
print(top_three)  # => Output: [9, 7, 5]

assert top_three == [9, 7, 5]  # => confirms the exact top-3 values in descending order
assert set(top_three) == {5, 7, 9}  # => cross-checks the SET of values, order aside
print("ex-39 OK")  # => Output: ex-39 OK
