# learning/code/ex-19-custom-marker-select/test_example.py
"""Example 19: A Custom Marker and -m Selection."""

import pytest  # => brings in @pytest.mark.slow -- a CUSTOM marker, registered in pytest.ini (co-08)


def fast_lookup(
    n: int,
) -> int:  # => a cheap, instant computation -- stands in for "fast" work
    return n * n  # => no sleep, no I/O -- genuinely fast


def heavy_computation(n: int) -> int:  # => stands in for "slow" work, without an ACTUAL sleep()  # fmt: skip
    return sum(range(n))  # => still fast in wall-clock time -- the MARKER, not real duration, is the point  # fmt: skip


def test_fast_lookup_always_runs() -> (
    None
):  # => no marker at all -- included in every run
    assert fast_lookup(5) == 25  # => a plain, unmarked test


@pytest.mark.slow  # => co-08: a CUSTOM label, meaningful only because of pytest.ini's registration  # fmt: skip
def test_heavy_computation_is_marked_slow() -> None:
    assert heavy_computation(100) == 4950  # => sum(range(100)) == 4950 -- still correct, just labeled  # fmt: skip
    # => running plain `pytest` executes BOTH tests; running `pytest -m "not slow"`
    # => excludes THIS test specifically, based purely on the marker name above
