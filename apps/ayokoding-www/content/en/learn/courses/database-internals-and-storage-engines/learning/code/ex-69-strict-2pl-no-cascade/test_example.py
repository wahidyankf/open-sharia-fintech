"""Example 69: pytest verification for Strict 2PL Preventing Cascading Aborts."""

import pytest

from example import LockConflictError, StrictTwoPhaseLockManager


def test_a_conflicting_write_lock_is_rejected_before_commit() -> None:
    manager = StrictTwoPhaseLockManager()
    manager.acquire_write("x", txn_id=1)
    with pytest.raises(LockConflictError):
        manager.acquire_write("x", txn_id=2)


def test_the_lock_becomes_available_only_after_commit() -> None:
    manager = StrictTwoPhaseLockManager()
    manager.acquire_write("x", txn_id=1)
    manager.commit(txn_id=1)
    manager.acquire_write(
        "x", txn_id=2
    )  # => no exception -- the lock was truly released at commit


# => Run: pytest -- Output: 2 passed
