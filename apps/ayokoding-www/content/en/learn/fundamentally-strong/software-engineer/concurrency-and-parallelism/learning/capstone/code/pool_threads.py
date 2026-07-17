"""Capstone: pool_threads.py -- Step 2a, the thread-pool version of the
I/O-bound fetch.

Verifies the SAME fetch, run through a ThreadPoolExecutor, matches
workload.py's baseline result exactly and beats its baseline time -- threads
DO help I/O-bound work (co-05): each fetch_page() call releases the GIL
during its time.sleep(), letting PAGE_COUNT threads' waits genuinely
overlap.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fetch itself

import time  # => time.perf_counter() -- the SAME timing harness workload.py's baseline uses
from concurrent.futures import ThreadPoolExecutor  # => co-23: a fixed-size pool of worker threads

from workload import PAGE_COUNT, fetch_page, run_serial_fetch  # => co-23: reuses Step 1's SAME fetch function + baseline


def run_threaded_fetch() -> tuple[float, list[int]]:  # => co-23/co-05: the pool-backed version of the SAME fetch
    start = time.perf_counter()  # => start: wall time before the pool-backed fetch begins
    with ThreadPoolExecutor(max_workers=PAGE_COUNT) as pool:  # => one worker PER page -- every fetch can overlap
        pages = list(pool.map(fetch_page, range(PAGE_COUNT)))  # => co-23: all PAGE_COUNT sleeps overlap, not serialize
    elapsed = time.perf_counter() - start  # => elapsed: expected close to ONE fetch_page() call, not PAGE_COUNT of them
    return elapsed, pages  # => (pool_time, pages) -- must match workload.py's (baseline_time, baseline_pages) shape


if __name__ == "__main__":  # => module entry point
    baseline_time, baseline_pages = run_serial_fetch()  # => baseline_time/baseline_pages: Step 1's serial ground truth
    pool_time, pool_pages = run_threaded_fetch()  # => pool_time/pool_pages: THIS step's pool-backed result
    print(f"serial={baseline_time:.2f}s threads={pool_time:.2f}s")  # => Output: serial=~0.40s threads=~0.05s

    # => co-05: fetching is I/O-bound, so a thread pool delivers a near-PAGE_COUNT-fold speedup -- each
    # => thread's time.sleep() releases the GIL, letting every page's simulated network wait overlap
    # => instead of stacking up. The RESULT is identical to the serial version either way (co-23 doesn't
    # => change WHAT gets fetched, only HOW LONG fetching all of it takes).
    assert pool_pages == baseline_pages  # => confirms the pool-backed fetch is EXACTLY as correct as the serial one
    assert pool_time < baseline_time / 2  # => confirms the pool delivered a genuine, substantial I/O speedup
    print("pool_threads.py OK")  # => Output: pool_threads.py OK
