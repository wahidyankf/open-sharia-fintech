# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 13: a deterministic calculation with no effects."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def total_after_discount(subtotal: int, percent: int) -> int:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return subtotal - subtotal * percent // 100


# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(total_after_discount(100, 10))
