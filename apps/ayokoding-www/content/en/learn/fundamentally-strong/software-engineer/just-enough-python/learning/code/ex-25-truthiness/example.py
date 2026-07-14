"""Example 25: Truthiness."""

# Empty collections, 0, "", and None are all falsy; everything else is truthy.
items: list[int] = []  # => an empty list -- falsy in a boolean context
if items:  # => equivalent to `if bool(items):` -- False for an empty collection
    print("has items")  # => never runs -- items is empty, so the condition is False
else:  # => runs because items is falsy
    print("empty")  # => Output: empty
