"""Example 11: pytest verification for A `Lock` Fixes the Racing Counter."""

from example import ITERATIONS_PER_THREAD, locked_total


def test_lock_produces_exactly_correct_total() -> None:
    expected = 2 * ITERATIONS_PER_THREAD
    actual = locked_total()
    assert actual == expected  # => no lost updates: the lock serializes every read-modify-write


def test_lock_is_reliable_across_repeated_runs() -> None:
    expected = 2 * ITERATIONS_PER_THREAD
    for _ in range(3):  # => repeats the race 3 times -- a lock's correctness must never be lucky
        assert locked_total() == expected


# => Run: pytest -- Output: 2 passed
