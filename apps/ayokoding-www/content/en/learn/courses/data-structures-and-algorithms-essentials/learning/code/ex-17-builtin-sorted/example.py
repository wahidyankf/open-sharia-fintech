"""Example 17: Built-in sorted()."""

# sorted() returns a NEW list; it never mutates its input -- Timsort, O(n log n) (co-15).
scores: list[int] = [5, 2, 9, 1, 7]  # => an unsorted list of ints
ascending = sorted(scores)  # => builds a brand-new list in ascending order
print(ascending)  # => Output: [1, 2, 5, 7, 9]
print(scores)  # => the original list is untouched -- Output: [5, 2, 9, 1, 7]

assert ascending == [1, 2, 5, 7, 9]  # => confirms every element landed in order
assert scores == [5, 2, 9, 1, 7]  # => confirms sorted() did not mutate the source
print("ex-17 OK")  # => Output: ex-17 OK
