"""Capstone: pool_process.py -- Step 3, the process-pool version of the
CPU-bound aggregation.

Compares THREE ways of running the SAME CPU-bound aggregation from
workload.py: strictly serial (the co-28 "one worker" baseline), a thread pool
(co-23 -- the GIL should prevent any real speedup), and a process pool
(co-24 -- each process has its OWN interpreter and OWN GIL, so this one
genuinely parallelizes). All three must produce the IDENTICAL aggregate.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the aggregation itself

import time  # => time.perf_counter() -- the SAME timing harness every capstone script reuses
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # => co-24 vs co-23, head to head

from workload import (  # => co-28: reuses Step 1's SAME workload shape + baseline, not a re-derived copy
    AGGREGATE_PROCESSORS,
    CPU_UNIT_ITERATIONS,
    PARALLEL_UNITS,
    SERIAL_UNITS,
    do_cpu_unit,
    run_serial_aggregate,
)


def amdahl_speedup(serial_fraction: float, processors: int) -> float:  # => co-28: Amdahl's Law's closed-form ceiling
    parallel_fraction = 1.0 - serial_fraction  # => the portion of the workload that DOES benefit from more workers
    return 1.0 / (serial_fraction + parallel_fraction / processors)  # => the theoretical MAXIMUM possible speedup


def run_threads_aggregate() -> tuple[float, int]:  # => co-23: same total work, pool-backed -- expected NOT to help
    start = time.perf_counter()  # => start: wall time before the serial-prefix + thread-pooled work begins
    total = do_cpu_unit(CPU_UNIT_ITERATIONS) * SERIAL_UNITS  # => the SERIAL_UNITS portion -- always runs first, sequentially
    with ThreadPoolExecutor(max_workers=AGGREGATE_PROCESSORS) as pool:  # => same worker count the process version uses
        total += sum(pool.map(do_cpu_unit, [CPU_UNIT_ITERATIONS] * PARALLEL_UNITS))  # => co-03: serialized by the GIL regardless
    elapsed = time.perf_counter() - start  # => elapsed: expected close to run_serial_aggregate's own one-worker time
    return elapsed, total  # => (threads_time, total) -- total must STILL match the serial baseline exactly


def run_processes_aggregate() -> tuple[float, int]:  # => co-24: same total work, GENUINELY parallel this time
    start = time.perf_counter()  # => start: wall time before the serial-prefix + process-pooled work begins
    total = do_cpu_unit(CPU_UNIT_ITERATIONS) * SERIAL_UNITS  # => the SAME inherently-serial portion, run first
    with ProcessPoolExecutor(max_workers=AGGREGATE_PROCESSORS) as pool:  # => EACH process gets its OWN interpreter, OWN GIL
        total += sum(pool.map(do_cpu_unit, [CPU_UNIT_ITERATIONS] * PARALLEL_UNITS))  # => co-24: genuinely overlaps across cores
    elapsed = time.perf_counter() - start  # => elapsed: expected well below the one-worker baseline, near the Amdahl ceiling
    return elapsed, total  # => (processes_time, total) -- total must match the serial baseline EXACTLY


if __name__ == "__main__":  # => module entry point
    one_worker_time, baseline_total = run_serial_aggregate()  # => Step 1's OWN aggregate baseline, reused verbatim
    threads_time, threads_total = run_threads_aggregate()  # => threads_time/threads_total: THIS step's thread-pooled result
    processes_time, processes_total = run_processes_aggregate()  # => processes_time/processes_total: THIS step's process-pooled result
    print(f"one_worker={one_worker_time:.2f}s threads={threads_time:.2f}s processes={processes_time:.2f}s")
    # => Output: one_worker=~1.00s threads=~1.00s processes=~0.40s

    serial_fraction = SERIAL_UNITS / (SERIAL_UNITS + PARALLEL_UNITS)  # => serial_fraction: co-28's "S", from THIS workload's own shape
    predicted_speedup = amdahl_speedup(serial_fraction, AGGREGATE_PROCESSORS)  # => predicted_speedup: the theoretical ceiling
    measured_speedup = one_worker_time / processes_time  # => measured_speedup: what ACTUALLY happened, empirically
    print(f"serial_fraction={serial_fraction:.2f} predicted={predicted_speedup:.2f}x measured={measured_speedup:.2f}x")
    # => Output: serial_fraction=0.20 predicted=2.50x measured=~2.1x-2.5x

    # => co-24/co-03: threads bring NO real speedup for CPU-bound work -- the GIL lets only one thread
    # => run Python bytecode at a time, so PARALLEL_UNITS worth of tight-loop arithmetic still runs
    # => essentially serially. Processes DO win: each worker gets its own interpreter and its own GIL,
    # => so the PARALLEL_UNITS portion genuinely overlaps across cores. Amdahl's Law (co-28) explains
    # => WHY the win is bounded at ~2.5x rather than 4x, even with 4 processors: SERIAL_UNITS is 1 of the
    # => 5 total units and can NEVER be parallelized away, capping the ceiling at 1/(0.2 + 0.8/4) = 2.5x --
    # => and the measured speedup lands close to that same theoretical ceiling, not just "faster".
    assert threads_total == baseline_total  # => confirms the thread-pooled aggregate is STILL exactly correct
    assert processes_total == baseline_total  # => confirms the process-pooled aggregate is STILL exactly correct
    assert threads_time > one_worker_time * 0.7  # => confirms threads did NOT deliver a meaningful CPU speedup
    assert processes_time < one_worker_time * 0.7  # => confirms processes DID deliver a meaningful CPU speedup
    assert measured_speedup > 1.5  # => confirms the process-pool speedup is real, not noise
    assert measured_speedup < predicted_speedup * 1.3  # => confirms the measured speedup stayed near the Amdahl ceiling
    print("pool_process.py OK")  # => Output: pool_process.py OK
