"""Example 20: Set Dedup."""

seen: set[int] = set([1, 1, 2, 3, 3])  # => set() drops duplicates -- keeps {1, 2, 3}
print(len(seen))  # => Output: 3
