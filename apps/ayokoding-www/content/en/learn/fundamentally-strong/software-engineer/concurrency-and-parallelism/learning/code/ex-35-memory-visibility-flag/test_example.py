"""Example 35: pytest verification for Memory Visibility -- Busy-Wait vs `Event`."""

import threading

from example import busy_wait_setter, busy_wait_waiter, event_setter, event_waiter


def test_busy_wait_eventually_observes_the_flip() -> None:
    flag = [False]
    observed: list[float] = []
    t1 = threading.Thread(target=busy_wait_waiter, args=(flag, observed))
    t2 = threading.Thread(target=busy_wait_setter, args=(flag, 0.05))
    t1.start()
    t2.start()
    t1.join(timeout=2)
    t2.join(timeout=2)
    assert observed and observed[0] < 1.0  # => the GIL made the unsynchronized write visible promptly


def test_event_wait_observes_the_set() -> None:
    event = threading.Event()
    observed: list[float] = []
    t1 = threading.Thread(target=event_waiter, args=(event, observed))
    t2 = threading.Thread(target=event_setter, args=(event, 0.05))
    t1.start()
    t2.start()
    t1.join(timeout=2)
    t2.join(timeout=2)
    assert observed and observed[0] < 1.0  # => the portable, correct tool works identically


# => Run: pytest -- Output: 2 passed
