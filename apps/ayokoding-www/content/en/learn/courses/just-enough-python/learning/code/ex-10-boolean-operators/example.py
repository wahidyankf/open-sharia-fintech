"""Example 10: Boolean Operators."""

# print() accepts multiple positional arguments and joins them with spaces.
# and/or/not are Python's three boolean operators (no bitwise-only forms needed here).
print(
    True and False,  # => and is True only if BOTH sides are True -- False
    True or False,  # => or is True if EITHER side is True -- True
    not True,  # => not flips a bool -- False
)  # => Output: False True False
