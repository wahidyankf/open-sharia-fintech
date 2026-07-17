"""Example 81: pytest verification for the Capstone-Preview Fetch-and-Aggregate Pipeline."""

import asyncio

from example import (
    AGGREGATE_CHUNKS,
    PAGE_COUNT,
    run_async_fetch,
    run_process_aggregate,
    run_serial_fetch,
    run_threaded_fetch,
    sum_of_squares,
)


def test_all_fetch_approaches_match_and_concurrent_ones_beat_serial() -> None:
    serial_time, serial_pages = run_serial_fetch()
    threaded_time, threaded_pages = run_threaded_fetch()
    async_time, async_pages = asyncio.run(run_async_fetch())

    expected_pages = [n * n for n in range(PAGE_COUNT)]
    assert serial_pages == expected_pages
    assert threaded_pages == expected_pages
    assert async_pages == expected_pages
    assert threaded_time < serial_time / 2  # => threads delivered the expected I/O speedup
    assert async_time < serial_time / 2  # => asyncio delivered the expected I/O speedup


def test_process_aggregate_matches_serial_aggregate() -> None:
    process_aggregate = run_process_aggregate()
    serial_aggregate = sum(sum_of_squares(chunk) for chunk in AGGREGATE_CHUNKS)
    assert process_aggregate == serial_aggregate  # => the parallel reduction matches the serial ground truth


# => Run: pytest -- Output: 2 passed
