"""Example 33: pytest verification for A Money Value Object with __eq__."""

from example import Money


def test_equal_amount_and_currency_compare_equal() -> None:
    assert Money(500, "USD") == Money(500, "USD")


def test_matching_amount_different_currency_compares_unequal() -> None:
    assert Money(500, "USD") != Money(500, "EUR")  # => amount alone is not enough


# => Run: pytest -- Output: 2 passed
