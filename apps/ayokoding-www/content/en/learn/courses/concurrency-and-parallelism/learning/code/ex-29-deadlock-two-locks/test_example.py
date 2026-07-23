"""Example 29: pytest verification for Two Threads, Two Locks, Opposite Order."""

from example import reproduce_deadlock


def test_opposite_lock_order_deterministically_deadlocks() -> None:
    a_hung, b_hung = reproduce_deadlock()
    assert a_hung is True  # => thread_a is permanently blocked waiting on lock_b
    assert b_hung is True  # => thread_b is permanently blocked waiting on lock_a


# => Run: pytest -- Output: 1 passed
