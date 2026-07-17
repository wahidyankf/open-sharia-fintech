"""Example 10: pytest verification for A Race's Output Is Nondeterministic Across Runs."""

from example import ITERATIONS_PER_THREAD, one_race


def test_repeated_races_produce_varying_totals() -> None:
    totals = [one_race() for _ in range(6)]
    expected = 2 * ITERATIONS_PER_THREAD
    assert len(set(totals)) > 1  # => the coin-flip jitter makes each run's interleaving different
    assert all(t <= expected for t in totals)  # => a race can only lose updates, never gain extra ones


# => Run: pytest -- Output: 1 passed
