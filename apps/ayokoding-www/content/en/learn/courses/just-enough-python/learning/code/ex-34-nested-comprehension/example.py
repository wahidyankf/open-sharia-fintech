"""Example 34: Nested Comprehension."""

matrix: list[list[int]] = [[1, 2], [3, 4]]  # => matrix is [[1, 2], [3, 4]]
# Two `for` clauses, outer then inner -- reads left to right.
flat: list[int] = [n for row in matrix for n in row]  # => flat is [1, 2, 3, 4]
print(flat)  # => Output: [1, 2, 3, 4]
