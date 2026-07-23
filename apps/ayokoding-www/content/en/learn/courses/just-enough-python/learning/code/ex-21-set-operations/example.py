"""Example 21: Set Operations."""

left: set[int] = {1, 2, 3}  # => left is {1, 2, 3} (type: set[int])
right: set[int] = {2, 3, 4}  # => right is {2, 3, 4} (type: set[int])
# Sets are unordered, so sorted() gives deterministic output for printing.
print(sorted(left | right))  # => union -- every element in either set -- [1, 2, 3, 4]
print(sorted(left & right))  # => intersection -- only elements in both -- [2, 3]
