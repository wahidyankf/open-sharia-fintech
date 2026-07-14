"""Example 29: List Comprehension."""

# Builds a list directly -- no append() build-up loop needed.
squares: list[int] = [n * n for n in range(5)]
print(squares)  # => Output: [0, 1, 4, 9, 16]
