"""Example 4: List Reverse via Slice."""

# lst[::-1] walks the list with step -1, building a brand-new reversed list (co-03).
original: list[int] = [1, 2, 3, 4]  # => original is [1, 2, 3, 4]
reversed_copy = original[::-1]  # => a NEW list, built by copying every element backward
print(reversed_copy)  # => Output: [4, 3, 2, 1]
print(original)  # => the source list is untouched -- Output: [1, 2, 3, 4]

assert reversed_copy == [4, 3, 2, 1]  # => confirms the new list is in reversed order
assert original == [1, 2, 3, 4]  # => confirms the original list was never mutated
assert reversed_copy is not original  # => confirms two distinct list objects exist
print("ex-04 OK")  # => Output: ex-04 OK
