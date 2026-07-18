"""Example 76: pytest verification for I/O Benchmarked Three Ways."""

import asyncio

from example import TASK_COUNT, run_asyncio, run_serial, run_threads


def test_both_concurrent_forms_beat_serial_on_io() -> None:
    serial_time, serial_results = run_serial()
    threads_time, threads_results = run_threads()
    asyncio_time, asyncio_results = asyncio.run(run_asyncio())

    expected = [n * n for n in range(TASK_COUNT)]
    assert threads_time < serial_time / 2  # => threads deliver a substantial I/O speedup
    assert asyncio_time < serial_time / 2  # => asyncio also delivers a substantial I/O speedup
    assert serial_results == expected
    assert threads_results == expected
    assert asyncio_results == expected


# => Run: pytest -- Output: 1 passed
