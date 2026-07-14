"""Example 32: Set Comprehension."""

# {} with no colon builds a set -- duplicates collapse automatically.
lengths: set[int] = {len(w) for w in ["a", "bb", "cc"]}
print(sorted(lengths))  # => "bb" and "cc" both have length 2 -- [1, 2]
