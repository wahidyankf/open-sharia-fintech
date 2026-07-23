"""Capstone: pytest verification for pool_threads.py's thread-pooled fetch."""

from pool_threads import run_threaded_fetch
from workload import run_serial_fetch


def test_threaded_fetch_matches_baseline_and_beats_it() -> None:
    baseline_time, baseline_pages = run_serial_fetch()
    pool_time, pool_pages = run_threaded_fetch()
    assert pool_pages == baseline_pages
    assert pool_time < baseline_time / 2  # => threads delivered a genuine I/O speedup


# => Run: pytest -- Output: 1 passed
