"""Example 71: pytest verification for An Order Enforcing Legal Status Transitions."""

import pytest

from example import Order


def test_legal_transition_succeeds() -> None:
    order: Order = Order()
    order.transition_to("shipped")
    assert order.status == "shipped"


def test_illegal_transition_raises() -> None:
    order: Order = Order()
    order.transition_to("shipped")
    with pytest.raises(ValueError):  # => shipped -> pending is not a legal transition
        order.transition_to("pending")


# => Run: pytest -- Output: 2 passed
