"""Example 24: pytest verification for Facade: One Call Hides Three Subsystems."""

# => this test deliberately imports ONLY CheckoutFacade -- never the three subsystems
from example import CheckoutFacade


def test_checkout_succeeds_with_a_single_call() -> None:
    facade: CheckoutFacade = CheckoutFacade()
    result: str = facade.checkout("widget", 2, 9.99)  # => the caller's only call
    assert result == "widget scheduled for delivery"  # => all three steps ran internally


def test_checkout_reports_out_of_stock_without_charging() -> None:
    facade: CheckoutFacade = CheckoutFacade()
    result: str = facade.checkout("widget", 999, 9.99)  # => fails the inventory step first
    assert result == "out of stock"  # => the caller sees a clean, single-string result


# => Run: pytest -- Output: 2 passed
