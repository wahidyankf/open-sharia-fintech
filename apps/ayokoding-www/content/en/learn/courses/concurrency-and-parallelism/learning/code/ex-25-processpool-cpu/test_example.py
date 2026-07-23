"""Example 25: pytest verification for `ProcessPoolExecutor` Beats Threads on CPU Work."""

import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from example import ITERATIONS, cpu_task


def test_process_pool_beats_thread_pool_on_cpu_work() -> None:
    task_count = 4
    start_threads = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as tp:
        list(tp.map(cpu_task, [ITERATIONS] * task_count))
    threads_time = time.perf_counter() - start_threads

    start_procs = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as pp:
        list(pp.map(cpu_task, [ITERATIONS] * task_count))
    procs_time = time.perf_counter() - start_procs

    assert procs_time < threads_time  # => processes sidestep the GIL; threads cannot


# => Run: pytest -- Output: 1 passed
