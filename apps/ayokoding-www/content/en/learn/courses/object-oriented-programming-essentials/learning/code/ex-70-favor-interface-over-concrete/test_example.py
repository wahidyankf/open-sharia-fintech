"""Example 70: pytest verification for Typing the Injected Field Against an Interface."""

from example import DiscountPricing, Order, PricingStrategy, RegularPricing


def test_any_conforming_implementation_is_accepted() -> None:
    strategies: list[PricingStrategy] = [RegularPricing(), DiscountPricing()]
    totals: list[float] = [Order(s).total(100.0) for s in strategies]
    assert totals == [
        100.0,
        80.0,
    ]  # => Order never mentions a concrete pricing class anywhere


# => Run: pytest -- Output: 1 passed
