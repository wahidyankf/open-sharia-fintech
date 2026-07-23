"""Example 14: pytest verification for Creator: Order Creates Its Own OrderLine."""

from example import Order, OrderLine


def test_order_add_line_is_the_creation_method() -> None:
    assert hasattr(Order, "add_line")  # => the creation method lives on Order itself


def test_add_line_both_builds_and_aggregates_the_line() -> None:
    order: Order = Order()
    line: OrderLine = order.add_line("widget", 3, 4.5)
    assert isinstance(line, OrderLine)  # => a real OrderLine was constructed
    assert order.lines == [line]  # => and it now lives inside Order's own collection


# => Run: pytest -- Output: 2 passed
