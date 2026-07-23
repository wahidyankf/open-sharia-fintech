"""Capstone: pytest verification for race_demo.py's race+fix and
deadlock+fix."""

from race_demo import (
    ITERATIONS_PER_THREAD,
    locked_total,
    no_longer_deadlocks,
    racing_total,
    reproduce_deadlock,
)


def test_unsynchronized_counter_loses_updates() -> None:
    expected = 2 * ITERATIONS_PER_THREAD
    actual = racing_total()
    assert actual < expected  # => the unsynchronized race reliably drops at least one increment


def test_locked_counter_is_exactly_correct() -> None:
    expected = 2 * ITERATIONS_PER_THREAD
    actual = locked_total()
    assert actual == expected  # => the lock eliminated every lost update


def test_two_lock_deadlock_reproduces() -> None:
    a_hung, b_hung = reproduce_deadlock()
    assert a_hung is True
    assert b_hung is True


def test_lock_ordering_resolves_the_deadlock() -> None:
    a_done, b_done = no_longer_deadlocks()
    assert a_done is True
    assert b_done is True


# => Run: pytest -- Output: 4 passed
