"""Example 83: pytest verification that the guard blocks ship() and each action fires exactly once."""

import pytest

from example import GuardBlocked, GuardedOrderFsm, IllegalTransition


def test_guard_blocks_ship_when_the_order_is_not_yet_paid() -> None:
    fsm = GuardedOrderFsm()
    fsm.send("confirm")
    with pytest.raises(GuardBlocked, match="not paid"):
        fsm.send("ship")  # => the table allows this transition; the GUARD is what blocks it
    assert fsm.state == "confirmed"  # => the state never advanced -- the guard fired before any mutation


def test_guard_passes_once_mark_paid_flips_the_independent_flag() -> None:
    fsm = GuardedOrderFsm()
    fsm.send("confirm")
    fsm.mark_paid()
    assert fsm.send("ship") == "shipped"


def test_entry_and_exit_actions_fire_exactly_once_per_state_crossing() -> None:
    fsm = GuardedOrderFsm()
    fsm.send("confirm")
    fsm.mark_paid()
    fsm.send("ship")
    fsm.send("deliver")
    assert fsm.entry_log == ["confirmed", "shipped", "delivered"]  # => exactly one entry per state entered
    assert fsm.exit_log == ["created", "confirmed", "shipped"]  # => exactly one exit per state left


def test_lock_released_flag_flips_on_the_first_exit_action() -> None:
    fsm = GuardedOrderFsm()
    assert fsm.lock_held is True  # => held from construction, before any transition
    fsm.send("confirm")
    assert fsm.lock_held is False  # => released by the exit action leaving "created"


def test_illegal_event_never_fires_a_guard_or_an_action() -> None:
    fsm = GuardedOrderFsm()
    with pytest.raises(IllegalTransition):
        fsm.send("deliver")  # => no table entry for ("created", "deliver") at all
    assert fsm.entry_log == []  # => no action fired for a transition the table itself rejected
    assert fsm.exit_log == []


# => Run: pytest -q -- Output: 5 passed
