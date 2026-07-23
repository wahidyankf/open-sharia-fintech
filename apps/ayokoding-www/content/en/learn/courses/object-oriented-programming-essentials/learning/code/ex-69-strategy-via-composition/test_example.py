"""Example 69: pytest verification for A Swappable Pricing Strategy via Composition."""

from example import DiscountPricing, Order, RegularPricing


def test_swapping_the_strategy_changes_the_computed_price() -> None:
    regular: Order = Order(RegularPricing())
    discounted: Order = Order(DiscountPricing())  # type: ignore
    assert regular.total(100.0) == 100.0
    assert discounted.total(100.0) == 80.0  # => zero subclassing of Order was needed


# => Run: pytest -- Output: 1 passed
