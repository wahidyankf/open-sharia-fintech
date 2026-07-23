"""Example 80: pytest verification for the Stress-Test Race Harness."""

from example import stress_test


def test_stress_harness_surfaces_the_race_in_the_unlocked_version() -> None:
    assert stress_test(worker_is_locked=False) > 0  # => at least one of the trials lost an update


def test_stress_harness_finds_no_failures_in_the_locked_version() -> None:
    assert stress_test(worker_is_locked=True) == 0  # => the lock-protected version never fails


# => Run: pytest -- Output: 2 passed
