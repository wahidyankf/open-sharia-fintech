"""Example 84: pytest verification that the FSM makes an illegal combination unrepresentable, unlike flags."""

import pytest

from example import (
    FlagOrder,
    IllegalTransition,
    OrderFsm,
    count_reachable_fsm_states,
    count_representable_flag_combinations,
)


def test_flag_order_can_represent_the_illegal_shipped_without_paid_combination() -> None:
    flags = FlagOrder()
    flags.is_shipped = True  # => nothing stops this -- the type itself allows the illegal combination
    assert flags.is_shipped is True
    assert flags.is_paid is False  # => the combination the business rules forbid IS representable in this type


def test_fsm_cannot_reach_shipped_without_first_passing_through_paid() -> None:
    fsm = OrderFsm()
    with pytest.raises(IllegalTransition, match="illegal in state 'created'"):
        fsm.send("ship")  # => structurally rejected -- there is no path to "shipped" that skips "paid"
    assert fsm.state == "created"  # => state never advanced


def test_fsm_reaches_shipped_only_via_the_paid_state() -> None:
    fsm = OrderFsm()
    fsm.send("pay")
    fsm.send("ship")
    assert fsm.state == "shipped"  # => the ONLY path to "shipped" passes through "paid"


def test_flag_soup_has_more_representable_combinations_than_the_fsm_has_reachable_states() -> None:
    assert count_representable_flag_combinations() == 8  # => every boolean combination is a distinct value
    assert count_reachable_fsm_states() == 5  # => strictly fewer -- illegal combinations simply do not exist


# => Run: pytest -q -- Output: 4 passed
