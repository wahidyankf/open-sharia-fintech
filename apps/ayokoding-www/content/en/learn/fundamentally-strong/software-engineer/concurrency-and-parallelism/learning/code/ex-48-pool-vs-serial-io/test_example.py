"""Example 48: pytest verification for Thread Pool vs Serial on I/O-Bound Work."""

import time
from concurrent.futures import ThreadPoolExecutor

from example import io_task


def test_thread_pool_is_substantially_faster_than_serial_on_io() -> None:
    task_count = 6
    start_serial = time.perf_counter()
    serial_results = [io_task(n) for n in range(task_count)]
    serial_time = time.perf_counter() - start_serial

    start_pool = time.perf_counter()
    with ThreadPoolExecutor(max_workers=task_count) as pool:
        pool_results = list(pool.map(io_task, range(task_count)))
    pool_time = time.perf_counter() - start_pool

    assert pool_time < serial_time / 2  # => overlapping I/O waits collapse the total wall time
    assert serial_results == pool_results  # => both approaches computed the identical correct results


# => Run: pytest -- Output: 1 passed
