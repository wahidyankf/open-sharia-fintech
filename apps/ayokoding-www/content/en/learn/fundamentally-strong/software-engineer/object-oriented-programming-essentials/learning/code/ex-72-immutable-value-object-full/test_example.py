"""Example 72: pytest verification for A Frozen Money Whose Arithmetic Returns New Instances."""

from example import Money


def test_plus_leaves_both_operands_unchanged() -> None:
    a: Money = Money(500)
    b: Money = Money(300)
    c: Money = a.plus(b)
    assert a.amount == 500  # => untouched
    assert b.amount == 300  # => untouched
    assert c.amount == 800  # => a brand-new object holding the sum


# => Run: pytest -- Output: 1 passed
