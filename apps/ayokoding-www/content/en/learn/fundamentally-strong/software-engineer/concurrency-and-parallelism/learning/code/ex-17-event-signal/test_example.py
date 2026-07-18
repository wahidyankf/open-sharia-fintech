"""Example 17: pytest verification for A `threading.Event` Signal."""

import threading

from example import signaler, waiter


def test_waiter_blocks_until_event_is_set() -> None:
    signal = threading.Event()
    log: list[str] = []
    t_wait = threading.Thread(target=waiter, args=(signal, log))
    t_signal = threading.Thread(target=signaler, args=(signal, 0.05))
    t_wait.start()
    t_signal.start()
    t_wait.join()
    t_signal.join()
    assert log == ["waiting", "proceeded"]  # => wait() only returns after set() is called


# => Run: pytest -- Output: 1 passed
