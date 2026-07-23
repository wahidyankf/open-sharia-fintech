"""Example 23: Slice String."""

word: str = "python"  # => word is "python" (type: str)
# Strings slice exactly like lists -- slicing never mutates the original string.
print(word[0:3])  # => characters 0, 1, 2 (stop is exclusive) -- "pyt"
