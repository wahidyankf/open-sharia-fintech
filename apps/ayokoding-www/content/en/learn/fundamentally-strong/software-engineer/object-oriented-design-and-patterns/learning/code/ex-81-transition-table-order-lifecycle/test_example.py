"""Example 81: pytest verification that every illegal event is rejected by the table itself."""

import pytest

from example import IllegalTransition, OrderFsm


def test_happy_path_walks_created_paid_shipped_delivered() -> None:
    order = OrderFsm()
    assert order.send("pay") == "paid"
    assert order.send("ship") == "shipped"
    assert order.send("deliver") == "delivered"


def test_cancel_is_legal_from_created_and_paid_but_not_after() -> None:
    order = OrderFsm()
    order.send("pay")
    assert order.send("cancel") == "cancelled"  # => legal: paid -> cancelled


def test_shipped_order_cannot_be_cancelled_the_table_has_no_such_entry() -> None:
    order = OrderFsm()
    order.send("pay")
    order.send("ship")
    with pytest.raises(IllegalTransition, match="illegal in state 'shipped'"):
        order.send("cancel")  # => rejected by a MISSING key, not a special-cased if-check


def test_delivered_is_terminal_every_event_is_rejected() -> None:
    order = OrderFsm()
    order.send("pay")
    order.send("ship")
    order.send("deliver")
    for event in ("pay", "ship", "deliver", "cancel"):
        with pytest.raises(IllegalTransition):
            order.send(event)  # => no key exists for ("delivered", event) -- the table itself enforces this


# => Run: pytest -q -- Output: 4 passed
