"""Example 45: pytest verification for the Strategy via typing.Protocol."""

from example import Order, discount_pricing, regular_pricing


def test_plain_function_satisfies_the_protocol_and_prices_regularly() -> None:
    order: Order = Order(regular_pricing)  # => a bare function, no inheritance declared
    assert order.total(100.0) == 100.0


def test_a_different_plain_function_satisfies_the_same_protocol() -> None:
    order: Order = Order(discount_pricing)  # => a DIFFERENT bare function, same shape
    assert order.total(100.0) == 80.0


# => Run: pytest -- Output: 2 passed
