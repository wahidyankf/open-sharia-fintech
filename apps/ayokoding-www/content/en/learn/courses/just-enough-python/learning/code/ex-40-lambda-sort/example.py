"""Example 40: Lambda Sort."""

pairs: list[tuple[str, int]] = [("b", 2), ("a", 1)]  # => pairs is [("b", 2), ("a", 1)]
# A lambda is a small anonymous function -- here, key=lambda p: p[0] extracts a sort key.
pairs.sort(key=lambda p: p[0])  # => key extracts the first element to sort by
print(pairs)  # => sorted by letter, not original order -- Output: [('a', 1), ('b', 2)]
