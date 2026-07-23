"""Example 60: pytest verification that state-object refactor makes illegal combos impossible."""

import pytest

from example import Created, FlagOrder, StateOrder


def test_flag_order_allows_the_illegal_shipped_without_paid_combination() -> None:
    order = FlagOrder()  # => reproduces the bug the refactor fixes
    order.mark_shipped()  # => nothing stops this even though is_paid is still False
    assert order.is_shipped is True and order.is_paid is False  # => the illegal combination exists


def test_state_order_rejects_shipping_before_payment() -> None:
    order = StateOrder()  # => starts in Created
    with pytest.raises(ValueError, match="not been paid"):  # => the illegal move is structurally rejected
        order.ship()
    assert isinstance(order.state, Created)  # => the order never left Created


def test_state_order_allows_the_legal_created_to_paid_to_shipped_path() -> None:
    order = StateOrder()
    order.pay()  # => Created -> Paid
    order.ship()  # => Paid -> Shipped
    assert order.state.name() == "Shipped"  # => reached the terminal state via only legal transitions


def test_state_order_rejects_paying_twice() -> None:
    order = StateOrder()
    order.pay()  # => first pay is legal
    with pytest.raises(ValueError, match="already paid"):  # => second pay is illegal
        order.pay()


# => Run: pytest -q -- Output: 4 passed
