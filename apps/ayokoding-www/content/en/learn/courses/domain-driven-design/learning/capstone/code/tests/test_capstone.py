"""Pin the capstone's tactical and strategic DDD boundaries without dependencies."""

from application import place_order
from domain.model import Money, Order, Quantity
from infrastructure import LegacyOrderDTO, MemoryOrderRepository, legacy_to_shipping


def test_aggregate_root_rejects_credit_limit_bypass() -> None:
    order = Order("o-1", Money(100))
    try:
        order.add_line(Quantity(2), Money(60))
    except ValueError as error:
        assert "credit limit" in str(error)
    else:
        raise AssertionError("aggregate root accepted an over-limit order")
    assert order.total == Money(0)


def test_repository_port_round_trips_valid_aggregate_and_event() -> None:
    order = Order("o-1", Money(100))
    order.add_line(Quantity(2), Money(25))
    repository = MemoryOrderRepository()
    events = place_order(order, repository)
    assert repository.get("o-1") is order
    assert events[0].order_id == "o-1" and events[0].total == Money(50)


def test_acl_translates_legacy_language_before_shipping_context() -> None:
    request = legacy_to_shipping(LegacyOrderDTO("o-1", 2))
    assert request.sales_order_id == "o-1" and request.quantity == 2


if __name__ == "__main__":
    test_aggregate_root_rejects_credit_limit_bypass()
    test_repository_port_round_trips_valid_aggregate_and_event()
    test_acl_translates_legacy_language_before_shipping_context()
    print("3 capstone assertions passed")
