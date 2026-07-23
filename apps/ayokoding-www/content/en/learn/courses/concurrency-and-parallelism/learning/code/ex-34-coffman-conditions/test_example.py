"""Example 34: pytest verification for The Four Coffman Conditions."""

from example import deadlock_conditions_all_present


def test_all_four_conditions_present_in_the_deadlocking_snapshot() -> None:
    snapshot = {"thread_a": "lock_a", "thread_a_wants": "lock_b", "thread_b": "lock_b"}
    conditions = deadlock_conditions_all_present(snapshot)
    assert all(conditions.values())  # => mutual_exclusion, hold_and_wait, no_preemption, circular_wait


def test_breaking_hold_and_wait_removes_one_condition() -> None:
    # => a snapshot where thread_a is NOT simultaneously waiting on lock_b
    snapshot = {"thread_a": "lock_a", "thread_a_wants": "nothing", "thread_b": "lock_b"}
    conditions = deadlock_conditions_all_present(snapshot)
    assert conditions["hold_and_wait"] is False  # => one broken condition is enough to prevent deadlock


# => Run: pytest -- Output: 2 passed
