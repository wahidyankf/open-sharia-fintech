"""Example 49: Threads Do NOT Speed Up CPU-Bound Work -- the GIL Serializes Them."""

import time  # => measures wall time to show threads barely beat serial on CPU work
from concurrent.futures import ThreadPoolExecutor  # => co-23: a pool of worker THREADS, not processes

TASK_COUNT = 4  # => how many independent CPU-bound tasks, both ways
ITERATIONS = 10_000_000  # => tuned so the difference (or lack of one) is clearly measurable


def cpu_task(n: int) -> int:  # => n: unused identifier -- pure CPU-bound busywork, no I/O anywhere
    total = 0  # => accumulator -- forces real interpreter bytecode execution, no shortcuts
    for i in range(n):  # => a tight loop -- the GIL cannot be released mid-iteration for pure Python code
        total += i  # => ordinary arithmetic on a LOCAL variable -- no shared state, no race here
    return total  # => only the TIME this takes matters for this example, not the value itself


if __name__ == "__main__":  # => module entry point
    start_serial = time.perf_counter()  # => start_serial: wall time before the ONE-AT-A-TIME loop
    serial_results = [cpu_task(ITERATIONS) for _ in range(TASK_COUNT)]  # => runs all TASK_COUNT calls in sequence
    serial_time = time.perf_counter() - start_serial  # => serial_time: the single-threaded baseline

    start_pool = time.perf_counter()  # => start_pool: wall time before the thread-pooled run
    with ThreadPoolExecutor(max_workers=TASK_COUNT) as pool:  # => TASK_COUNT threads, ONE shared interpreter
        pool_results = list(pool.map(cpu_task, [ITERATIONS] * TASK_COUNT))  # => all TASK_COUNT calls "concurrent"
    pool_time = time.perf_counter() - start_pool  # => pool_time: expected close to serial_time, not a fraction of it

    print(f"serial={serial_time:.2f}s pool={pool_time:.2f}s")  # => Output: serial=~0.60s pool=~0.65s (roughly equal)

    # => The Global Interpreter Lock (co-03) allows only ONE thread to execute Python bytecode at a time,
    # => no matter how many threads exist or how many CPU cores are available. For pure CPU-bound work
    # => like this tight loop, there is no I/O wait to release the GIL during (contrast ex-48, where
    # => `time.sleep` DOES release it) -- so a thread pool provides essentially NO speedup here, and can
    # => even be slightly SLOWER than serial due to thread-switching overhead. `ProcessPoolExecutor`
    # => (ex-25, ex-49's natural companion) is the fix, since each process gets its OWN GIL (co-24).
    assert pool_time > serial_time * 0.7  # => confirms threads did NOT deliver a meaningful speedup
    assert serial_results == pool_results  # => confirms both approaches still computed the identical result
    print("ex-49 OK")  # => Output: ex-49 OK
