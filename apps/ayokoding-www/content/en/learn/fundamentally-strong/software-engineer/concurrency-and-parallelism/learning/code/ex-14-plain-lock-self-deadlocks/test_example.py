"""Example 14: pytest verification for A Plain `Lock` Self-Deadlocks on Re-Acquire."""

import threading

from example import try_reacquire_same_thread


def test_plain_lock_blocks_on_same_thread_reacquire() -> None:
    lock = threading.Lock()
    succeeded = try_reacquire_same_thread(lock, timeout=0.2)
    assert succeeded is False  # => a plain Lock cannot tell "same thread" from "different thread"
    assert lock.locked() is False  # => the final release() left it clean for the next test


# => Run: pytest -- Output: 1 passed
