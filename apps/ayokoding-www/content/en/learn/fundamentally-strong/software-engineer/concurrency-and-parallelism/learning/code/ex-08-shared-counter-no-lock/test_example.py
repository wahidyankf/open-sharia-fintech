"""Example 8: pytest verification for A Shared Counter Without a Lock Loses Updates."""

from example import ITERATIONS_PER_THREAD, racing_total


def test_unsynchronized_counter_loses_updates() -> None:
    expected = 2 * ITERATIONS_PER_THREAD
    actual = racing_total()
    assert actual < expected  # => the unsynchronized race reliably drops at least one increment


# => Run: pytest -- Output: 1 passed
