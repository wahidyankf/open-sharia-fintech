"""Example 25: `ProcessPoolExecutor` Beats Threads on CPU Work."""

import time  # => measures wall time to compare the two pool types
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # => co-24 vs co-23

ITERATIONS = 15_000_000  # => tuned so 4 tasks take a small but clearly measurable amount of time


def cpu_task(n: int) -> int:  # => pure CPU work -- the GIL serializes this on THREADS (co-03)
    total = 0  # => total is 0 -- accumulator forcing real interpreter work
    for i in range(n):  # => a tight loop -- exactly the shape the GIL cannot parallelize on threads
        total += i  # => non-atomic arithmetic, but this example doesn't share it across tasks
    return total  # => the value itself is irrelevant -- only the TIME spent doing it matters here


if __name__ == "__main__":  # => module entry point
    task_count = 4  # => 4 independent CPU-bound tasks, run both ways

    start_threads = time.perf_counter()  # => start_threads: wall time before the thread-pool run
    with ThreadPoolExecutor(max_workers=4) as thread_pool:  # => 4 threads, same interpreter, ONE GIL
        list(thread_pool.map(cpu_task, [ITERATIONS] * task_count))  # => runs all 4, serialized by the GIL
    threads_time = time.perf_counter() - start_threads  # => threads_time: barely faster than serial

    start_procs = time.perf_counter()  # => start_procs: wall time before the process-pool run
    with ProcessPoolExecutor(max_workers=4) as proc_pool:  # => 4 processes, EACH with its OWN GIL (co-24)
        list(proc_pool.map(cpu_task, [ITERATIONS] * task_count))  # => genuinely runs on separate cores
    procs_time = time.perf_counter() - start_procs  # => procs_time: close to 1/4 of threads_time

    print(f"threads={threads_time:.2f}s procs={procs_time:.2f}s")  # => Output: threads=~1.2s procs=~0.4s

    # => Threads all share ONE interpreter and ONE GIL, so 4 CPU-bound tasks on threads run barely
    # => faster than running them one after another. Processes each get their OWN interpreter and
    # => OWN GIL, sidestepping the GIL entirely -- so the process pool genuinely uses multiple cores.
    assert procs_time < threads_time  # => confirms the process pool measurably beat the thread pool
    print("ex-25 OK")  # => Output: ex-25 OK
