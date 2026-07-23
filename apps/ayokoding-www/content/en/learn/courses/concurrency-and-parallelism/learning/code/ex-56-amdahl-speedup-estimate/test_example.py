"""Example 56: pytest verification for Amdahl's Law Speedup Prediction."""

from example import amdahl_speedup


def test_zero_serial_fraction_gives_full_linear_speedup() -> None:
    assert amdahl_speedup(serial_fraction=0.0, processors=4) == 4.0  # => no serial bottleneck -- full 4x


def test_fully_serial_workload_gives_no_speedup() -> None:
    assert amdahl_speedup(serial_fraction=1.0, processors=4) == 1.0  # => 100% serial -- more processors never help


def test_partial_serial_fraction_matches_the_closed_form() -> None:
    # => S=0.2, N=4: 1 / (0.2 + 0.8/4) = 1 / 0.4 = 2.5
    assert amdahl_speedup(serial_fraction=0.2, processors=4) == 2.5


# => Run: pytest -- Output: 3 passed
