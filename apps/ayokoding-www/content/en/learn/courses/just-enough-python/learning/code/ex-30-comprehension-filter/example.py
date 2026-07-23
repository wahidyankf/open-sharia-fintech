"""Example 30: Comprehension Filter."""

# The `if` filters BEFORE an n is kept.
evens: list[int] = [n for n in range(6) if n % 2 == 0]
print(evens)  # => Output: [0, 2, 4]
