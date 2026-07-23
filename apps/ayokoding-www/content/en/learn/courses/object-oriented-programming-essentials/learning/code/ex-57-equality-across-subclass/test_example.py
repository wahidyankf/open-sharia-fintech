"""Example 57: pytest verification for A Type-Strict __eq__ Across a Subclass."""

from example import Cash, Money


def test_type_strict_eq_rejects_cross_subclass_comparison() -> None:
    m: Money = Money(500)
    c: Cash = Cash(500)  # => same amount, different exact type
    assert m != c  # => the chosen (type-strict) contract holds


def test_same_exact_type_still_compares_by_value() -> None:
    assert Money(500) == Money(500)  # => same exact type, same amount -- equal


# => Run: pytest -- Output: 2 passed
