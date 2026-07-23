"""Example 30: pytest verification for A Global Lock Order Fixes the Deadlock."""

from example import no_longer_deadlocks


def test_consistent_lock_order_prevents_deadlock() -> None:
    a_done, b_done = no_longer_deadlocks()
    assert a_done is True  # => a consistent global order broke the circular-wait condition
    assert b_done is True


# => Run: pytest -- Output: 1 passed
