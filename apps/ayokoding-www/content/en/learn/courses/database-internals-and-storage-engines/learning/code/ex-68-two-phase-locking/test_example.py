"""Example 68: pytest verification for Two-Phase Locking."""

import pytest

from example import Transaction, TwoPhaseLockError


def test_acquiring_during_the_growing_phase_succeeds() -> None:
    txn = Transaction()
    txn.acquire("a")
    txn.acquire("b")
    assert txn.held == {"a", "b"}


def test_acquiring_after_the_first_release_raises() -> None:
    txn = Transaction()
    txn.acquire("a")
    txn.release("a")
    with pytest.raises(TwoPhaseLockError):
        txn.acquire("b")


# => Run: pytest -- Output: 2 passed
