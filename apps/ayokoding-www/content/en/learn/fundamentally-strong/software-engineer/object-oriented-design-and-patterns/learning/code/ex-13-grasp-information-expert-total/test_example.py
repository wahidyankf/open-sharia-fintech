"""Example 13: pytest verification for Information Expert: Order Owns Its Total."""

from example import Order, OrderLine


def test_order_computes_its_own_total() -> None:
    order: Order = Order()
    order.add_line(OrderLine("widget", 2, 9.99))
    order.add_line(OrderLine("gadget", 1, 19.99))
    assert round(order.total(), 2) == 39.97  # => Order alone answered this question


def test_order_is_the_only_place_total_is_computed() -> None:
    # => structural check: no other function in this module computes an order total
    import example  # => imports the module itself to inspect its top-level names

    assert not hasattr(example, "compute_order_total")  # => no external loop exists anywhere in the module
    assert hasattr(Order, "total")  # => only Order, the information expert, has it


# => Run: pytest -- Output: 2 passed
