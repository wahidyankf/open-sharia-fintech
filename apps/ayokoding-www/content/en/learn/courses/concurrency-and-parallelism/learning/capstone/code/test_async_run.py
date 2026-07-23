"""Capstone: pytest verification for async_run.py's asyncio-based fetch."""

import asyncio

from async_run import run_async_fetch
from workload import run_serial_fetch


def test_async_fetch_matches_baseline_and_beats_it() -> None:
    baseline_time, baseline_pages = run_serial_fetch()
    async_time, async_pages = asyncio.run(run_async_fetch())
    assert async_pages == baseline_pages
    assert async_time < baseline_time / 2  # => asyncio delivered a genuine I/O speedup


# => Run: pytest -- Output: 1 passed
