"""Example 49: pytest verification for Threads NOT Speeding Up CPU-Bound Work."""

import time
from concurrent.futures import ThreadPoolExecutor

from example import cpu_task

ITERATIONS = 8_000_000


def test_thread_pool_does_not_meaningfully_beat_serial_on_cpu_work() -> None:
    task_count = 4
    start_serial = time.perf_counter()
    serial_results = [cpu_task(ITERATIONS) for _ in range(task_count)]
    serial_time = time.perf_counter() - start_serial

    start_pool = time.perf_counter()
    with ThreadPoolExecutor(max_workers=task_count) as pool:
        pool_results = list(pool.map(cpu_task, [ITERATIONS] * task_count))
    pool_time = time.perf_counter() - start_pool

    assert pool_time > serial_time * 0.6  # => no meaningful speedup -- the GIL serializes CPU-bound threads
    assert serial_results == pool_results  # => both approaches still computed the identical result


# => Run: pytest -- Output: 1 passed
