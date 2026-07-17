"""Capstone: workload.py -- the serial baseline + a timing harness.

Defines the two workloads this capstone measures three ways (threads,
asyncio, processes) against this file's own serial baseline: an I/O-bound
page fetch and a CPU-bound aggregation. Every other capstone script imports
its workload functions and its baseline timings from HERE, so "the correct
aggregate" always means: matches what THIS file computes, run one step at a
time, with nothing overlapping.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the workload itself

import time  # => time.perf_counter() -- the SAME timing harness every capstone script reuses

# --- I/O-bound workload: fetching PAGE_COUNT "pages" -----------------------

PAGE_COUNT = 8  # => co-05: how many simulated pages to fetch, all THREE fetch ways (serial/threads/asyncio)
FETCH_DELAY = 0.05  # => simulated per-page network latency -- large enough that overlap is clearly measurable


def fetch_page(page_number: int) -> int:  # => co-05/co-06: the SYNCHRONOUS fetch every non-async script reuses
    time.sleep(FETCH_DELAY)  # => simulates the I/O wait a real network call would genuinely block on
    return page_number * page_number  # => a trivial, checkable "payload size" -- correctness is easy to assert


def run_serial_fetch() -> tuple[float, list[int]]:  # => co-05: THE baseline every other fetch approach is compared against
    start = time.perf_counter()  # => start: wall time before the strictly-sequential fetch loop
    pages = [fetch_page(n) for n in range(PAGE_COUNT)]  # => fetches EVERY page one at a time -- no overlap possible
    elapsed = time.perf_counter() - start  # => elapsed: the serial I/O baseline -- PAGE_COUNT * FETCH_DELAY, roughly
    return elapsed, pages  # => (baseline_time, correct_pages) -- what pool_threads.py/async_run.py must match


# --- CPU-bound workload: aggregating SERIAL_UNITS + PARALLEL_UNITS "units" -

CPU_UNIT_ITERATIONS = 6_000_000  # => tuned so ONE unit's cost is clearly measurable, not dominated by overhead
SERIAL_UNITS = 1  # => co-28: work that CANNOT be parallelized -- e.g. merging fetched pages before aggregation starts
PARALLEL_UNITS = 4  # => co-28: work that CAN be split across independent workers
AGGREGATE_PROCESSORS = 4  # => how many worker processes/threads pool_process.py actually uses


def do_cpu_unit(iterations: int) -> int:  # => co-24: a top-level function -- REQUIRED so ProcessPoolExecutor can pickle it
    total = 0  # => accumulator -- forces real interpreter bytecode work, the shape a GIL serializes across threads (co-03)
    for i in range(iterations):  # => a tight loop -- deliberately CPU-bound, no I/O wait to release the GIL during
        total += i  # => trivial arithmetic; only the TIME this consumes and its (deterministic) VALUE matter here
    return total  # => deterministic: n*(n-1)//2 -- every concurrency model below must return this EXACT total


def run_serial_aggregate() -> tuple[float, int]:  # => co-28: the "one worker" baseline -- everything strictly sequential
    start = time.perf_counter()  # => start: wall time before ANY unit runs
    total = 0  # => total: the running sum across every unit, serial and parallel alike
    for _ in range(SERIAL_UNITS + PARALLEL_UNITS):  # => with ONE worker, nothing can overlap -- ALL units run in turn
        total += do_cpu_unit(CPU_UNIT_ITERATIONS)  # => the SAME unit function every other approach below also calls
    elapsed = time.perf_counter() - start  # => elapsed: the one-worker Amdahl baseline (co-28) AND the serial baseline
    return elapsed, total  # => (baseline_time, correct_total) -- what pool_process.py's variants must match EXACTLY


def run_serial_pipeline() -> tuple[float, list[int], int]:  # => Step 1: the FULL serial baseline -- fetch, THEN aggregate
    fetch_time, pages = run_serial_fetch()  # => fetch_time: I/O-bound half, strictly sequential
    aggregate_time, total = run_serial_aggregate()  # => aggregate_time: CPU-bound half, strictly sequential
    return fetch_time + aggregate_time, pages, total  # => (whole-pipeline time, correct pages, correct aggregate)


if __name__ == "__main__":  # => module entry point
    elapsed, pages, total = run_serial_pipeline()  # => the single source of truth every other script cross-checks against
    print(f"serial pipeline: {elapsed:.2f}s")  # => Output: serial pipeline: ~0.65s (0.40s fetch + 0.25s aggregate)
    print(f"pages={pages}")  # => Output: pages=[0, 1, 4, 9, 16, 25, 36, 49]
    print(f"aggregate={total}")  # => Output: aggregate=<deterministic int, see below>

    expected_pages = [n * n for n in range(PAGE_COUNT)]  # => expected_pages: the ground-truth fetch result
    expected_unit = CPU_UNIT_ITERATIONS * (CPU_UNIT_ITERATIONS - 1) // 2  # => closed-form sum(range(n)) for ONE unit
    expected_total = expected_unit * (SERIAL_UNITS + PARALLEL_UNITS)  # => (SERIAL_UNITS + PARALLEL_UNITS) IDENTICAL units
    assert pages == expected_pages  # => confirms the serial fetch produced exactly the expected pages
    assert total == expected_total  # => confirms the serial aggregate matches the closed-form ground truth EXACTLY
    print("workload.py OK")  # => Output: workload.py OK
