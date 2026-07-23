"""Capstone: async_run.py -- Step 2b, the asyncio version of the I/O-bound
fetch.

Verifies a COOPERATIVE, single-threaded asyncio.gather() fetch matches
workload.py's baseline result exactly and beats its baseline time --
asyncio.sleep() yields the event loop instead of blocking a thread, so
PAGE_COUNT "network waits" overlap on ONE thread, no thread pool required
(co-26/co-05).
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fetch itself

import asyncio  # => co-26: async/await + the event loop driving this cooperative fetch
import time  # => time.perf_counter() -- the SAME timing harness workload.py's baseline uses

from workload import FETCH_DELAY, PAGE_COUNT, run_serial_fetch  # => co-26: reuses Step 1's SAME constants + baseline


async def fetch_page_async(page_number: int) -> int:  # => co-26: the COOPERATIVE counterpart to workload.py's fetch_page
    await asyncio.sleep(FETCH_DELAY)  # => the IDENTICAL simulated delay, yielded cooperatively instead of blocking
    return page_number * page_number  # => the SAME result shape as workload.py's fetch_page -- correctness must match


async def run_async_fetch() -> tuple[float, list[int]]:  # => co-26: gathers ALL PAGE_COUNT fetches concurrently
    start = time.perf_counter()  # => start: wall time before the gather begins
    pages = await asyncio.gather(*(fetch_page_async(n) for n in range(PAGE_COUNT)))  # => co-26: every sleep overlaps on ONE thread
    elapsed = time.perf_counter() - start  # => elapsed: expected close to ONE fetch's delay, like pool_threads.py's result
    return elapsed, list(pages)  # => (async_time, pages) -- must match workload.py's (baseline_time, baseline_pages) shape


if __name__ == "__main__":  # => module entry point
    baseline_time, baseline_pages = run_serial_fetch()  # => baseline_time/baseline_pages: Step 1's serial ground truth
    async_time, async_pages = asyncio.run(run_async_fetch())  # => async_time/async_pages: THIS step's coroutine-based result
    print(f"serial={baseline_time:.2f}s asyncio={async_time:.2f}s")  # => Output: serial=~0.40s asyncio=~0.05s

    # => co-26/co-27: asyncio delivers the SAME I/O-bound speedup as pool_threads.py's thread pool, but
    # => cooperatively -- ONE thread, ONE event loop, and every fetch_page_async() call VOLUNTARILY yields
    # => at its `await asyncio.sleep(...)`, letting the loop start the next fetch instead of blocking.
    # => No GIL contention, no thread-pool bookkeeping -- just N coroutines taking turns on one thread.
    assert async_pages == baseline_pages  # => confirms the asyncio fetch is EXACTLY as correct as the serial one
    assert async_time < baseline_time / 2  # => confirms asyncio delivered a genuine, substantial I/O speedup
    print("async_run.py OK")  # => Output: async_run.py OK
