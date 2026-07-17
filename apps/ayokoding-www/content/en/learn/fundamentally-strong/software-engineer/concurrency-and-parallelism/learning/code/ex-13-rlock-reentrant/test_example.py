"""Example 13: pytest verification for `RLock` Lets the Owning Thread Re-Acquire."""

import threading

from example import outer


def test_same_thread_reacquires_rlock_without_deadlock() -> None:
    rl = threading.RLock()
    log: list[str] = []
    outer(rl, log)  # => if RLock were a plain Lock, this call would hang forever
    assert log == ["outer-acquired", "inner-acquired"]


# => Run: pytest -- Output: 1 passed
