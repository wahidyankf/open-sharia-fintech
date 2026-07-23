"""Example 71: pytest verification for Work-Stealing Load Balancing."""

from collections import deque

from example import simulate_work_stealing


def test_idle_worker_steals_work_and_load_balances() -> None:
    worker_a: "deque[int]" = deque(range(1))
    worker_b: "deque[int]" = deque(range(9))
    completed_a, completed_b, steal_events = simulate_work_stealing(worker_a, worker_b)

    assert completed_a + completed_b == 10  # => every task processed exactly once
    assert completed_a > 1  # => worker "a" processed more than its own original 1 task -- it stole work
    assert len(steal_events) > 0  # => stealing genuinely happened


# => Run: pytest -- Output: 1 passed
