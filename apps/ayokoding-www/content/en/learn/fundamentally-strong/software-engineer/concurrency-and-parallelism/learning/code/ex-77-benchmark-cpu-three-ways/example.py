"""Example 77: CPU-Bound Work, Benchmarked Three Ways -- Only Processes Actually Win."""

import time  # => measures wall time across all three approaches
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # => co-24 vs co-23

TASK_COUNT = 4  # => how many independent CPU-bound tasks, all THREE ways
ITERATIONS = 8_000_000  # => tuned so the difference between approaches is clearly measurable


def cpu_task(n: int) -> int:  # => a top-level function -- REQUIRED so ProcessPoolExecutor can pickle it
    total = 0  # => accumulator -- forces real interpreter bytecode execution
    for i in range(n):  # => a tight loop -- the shape a GIL serializes across threads (co-03)
        total += i  # => trivial arithmetic; only the TIME this takes matters here
    return total  # => the actual value is irrelevant to this example


def run_serial() -> float:
    start = time.perf_counter()  # => start: wall time before the ONE-AT-A-TIME loop
    for _ in range(TASK_COUNT):  # => runs every task strictly in sequence, on this ONE thread
        cpu_task(ITERATIONS)  # => no overlap possible -- this IS the baseline every other approach is measured against
    return time.perf_counter() - start  # => serial_time: the single-threaded baseline


def run_threads() -> float:
    start = time.perf_counter()  # => start: wall time before the thread-pooled run
    with ThreadPoolExecutor(max_workers=TASK_COUNT) as pool:  # => TASK_COUNT threads, ONE shared interpreter
        list(pool.map(cpu_task, [ITERATIONS] * TASK_COUNT))  # => serialized by the GIL despite "running concurrently"
    return time.perf_counter() - start  # => threads_time: expected close to serial_time (co-05 does NOT apply here)


def run_processes() -> float:
    start = time.perf_counter()  # => start: wall time before the process-pooled run
    with ProcessPoolExecutor(max_workers=TASK_COUNT) as pool:  # => TASK_COUNT processes, EACH with its OWN GIL
        list(pool.map(cpu_task, [ITERATIONS] * TASK_COUNT))  # => genuinely runs across multiple cores
    return time.perf_counter() - start  # => processes_time: expected substantially FASTER than serial_time


if __name__ == "__main__":  # => module entry point
    serial_time = run_serial()  # => serial_time: the single-threaded baseline
    threads_time = run_threads()  # => threads_time: the multi-threaded CPU run
    processes_time = run_processes()  # => processes_time: the multi-process CPU run

    print(f"serial={serial_time:.2f}s threads={threads_time:.2f}s processes={processes_time:.2f}s")
    # => Output: serial=~1.0s threads=~1.0s processes=~0.35s

    # => Unlike ex-76's I/O-bound benchmark, where BOTH concurrency models won, CPU-bound work behaves
    # => very differently: threads provide essentially NO speedup because the GIL serializes their Python
    # => bytecode regardless of how many threads exist (co-03, co-05 doesn't apply -- there's no I/O wait
    # => to release the GIL during). Only `ProcessPoolExecutor` (co-24) genuinely wins, because each
    # => process gets its OWN interpreter and OWN GIL, sidestepping the single-GIL bottleneck entirely.
    assert threads_time > serial_time * 0.7  # => confirms threads did NOT deliver a meaningful CPU speedup
    assert processes_time < serial_time * 0.7  # => confirms processes DID deliver a meaningful CPU speedup
    print("ex-77 OK")  # => Output: ex-77 OK
