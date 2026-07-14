"""Example 13: Deduplicate a List with a Set."""

# set() collapses duplicates because a set can only hold each hash-equal
# value once -- turning "remove duplicates" into a single constructor call (co-09).
raw: list[int] = [1, 2, 2, 3, 1, 4, 3]  # => raw has 7 elements, 4 of them unique
unique_values = set(raw)  # => builds a set, silently dropping every repeat
unique_count = len(unique_values)  # => the set's size is exactly the unique count
print(unique_values)  # => Output: {1, 2, 3, 4} (set order is not guaranteed)
print(unique_count)  # => Output: 4

assert unique_count == 4  # => confirms exactly 4 distinct values existed in raw
assert unique_values == {1, 2, 3, 4}  # => confirms the exact set of unique values
print("ex-13 OK")  # => Output: ex-13 OK
