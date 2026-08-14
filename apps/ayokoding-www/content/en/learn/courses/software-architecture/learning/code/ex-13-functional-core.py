"""Worked Example 13: a deterministic calculation with no effects."""


def total_after_discount(subtotal: int, percent: int) -> int:
    return subtotal - subtotal * percent // 100


print(total_after_discount(100, 10))
