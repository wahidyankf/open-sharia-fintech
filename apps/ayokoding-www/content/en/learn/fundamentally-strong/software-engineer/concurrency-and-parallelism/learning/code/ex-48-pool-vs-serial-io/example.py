"""Example 48: A Thread Pool Beats Serial Execution on I/O-Bound Work."""

import time  # => `time.sleep` simulates I/O -- network calls, disk reads, anything that BLOCKS but doesn't compute
from concurrent.futures import ThreadPoolExecutor  # => co-23: a pool of worker threads

TASK_COUNT = 8  # => how many independent "I/O calls" to make, both ways
SLEEP_SECONDS = 0.1  # => how long EACH simulated I/O call blocks -- the GIL is released during real sleep


def io_task(n: int) -> int:  # => n: an identifier, unused in the computation -- only the delay matters here
    time.sleep(SLEEP_SECONDS)  # => simulates a blocking I/O wait -- releases the GIL for this duration (co-05)
    return n * n  # => a trivial "result" so this function still returns something meaningful


if __name__ == "__main__":  # => module entry point
    start_serial = time.perf_counter()  # => start_serial: wall time before the ONE-AT-A-TIME loop
    serial_results = [io_task(n) for n in range(TASK_COUNT)]  # => runs all TASK_COUNT calls strictly in sequence
    serial_time = time.perf_counter() - start_serial  # => serial_time: roughly TASK_COUNT * SLEEP_SECONDS

    start_pool = time.perf_counter()  # => start_pool: wall time before the pooled run
    with ThreadPoolExecutor(max_workers=TASK_COUNT) as pool:  # => enough workers to run every task at once
        pool_results = list(pool.map(io_task, range(TASK_COUNT)))  # => all TASK_COUNT calls OVERLAP in time
    pool_time = time.perf_counter() - start_pool  # => pool_time: close to ONE SLEEP_SECONDS, not TASK_COUNT of them

    print(f"serial={serial_time:.2f}s pool={pool_time:.2f}s")  # => Output: serial=~0.80s pool=~0.10s

    # => I/O-bound work spends most of its time WAITING, not computing -- and `time.sleep` (like a real
    # => network call) releases the GIL while it waits (co-05). A `ThreadPoolExecutor` exploits this: all
    # => TASK_COUNT threads can be "sleeping" (i.e., blocked on I/O) AT THE SAME TIME, so the total wall
    # => time collapses to roughly ONE task's duration instead of the sum of all of them. This is exactly
    # => the case where THREADS help despite the GIL (contrast ex-49, where they don't help CPU work).
    assert pool_time < serial_time / 2  # => confirms the pool is substantially faster, not just marginally
    assert serial_results == pool_results  # => confirms BOTH approaches computed the identical correct results
    print("ex-48 OK")  # => Output: ex-48 OK
