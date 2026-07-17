"""Example 81: Capstone Preview -- Fetch-and-Aggregate, Three Ways, One Timing Harness."""

import asyncio  # => co-26: the async fetch approach
import time  # => measures wall time across every approach
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # => co-23 (fetch) and co-24 (aggregate)

PAGE_COUNT = 6  # => how many simulated "pages" to fetch, all THREE fetch ways
FETCH_DELAY = 0.06  # => simulated network latency per page
AGGREGATE_CHUNKS = [list(range(i * 1000, (i + 1) * 1000)) for i in range(4)]  # => a CPU-bound reduction workload


def fetch_page_sync(n: int) -> int:  # => the SYNCHRONOUS fetch -- used by both serial and threaded runs
    time.sleep(FETCH_DELAY)  # => simulates the I/O wait every "page fetch" would genuinely block on
    return n * n  # => a trivial per-page "payload size" so results can be checked


async def fetch_page_async(n: int) -> int:  # => the COOPERATIVE fetch -- used by the asyncio run
    await asyncio.sleep(FETCH_DELAY)  # => the SAME delay, yielded cooperatively instead of blocking
    return n * n  # => identical result shape to the synchronous version


def sum_of_squares(chunk: list[int]) -> int:  # => a top-level function -- REQUIRED for ProcessPoolExecutor
    return sum(x * x for x in chunk)  # => the CPU-bound "aggregate" step -- co-24's territory, not I/O


def run_serial_fetch() -> tuple[float, list[int]]:
    start = time.perf_counter()  # => start: wall time before the serial fetch loop
    pages = [fetch_page_sync(n) for n in range(PAGE_COUNT)]  # => fetches every page strictly one at a time
    return time.perf_counter() - start, pages  # => elapsed time AND the fetched results


def run_threaded_fetch() -> tuple[float, list[int]]:
    start = time.perf_counter()  # => start: wall time before the thread-pooled fetch
    with ThreadPoolExecutor(max_workers=PAGE_COUNT) as pool:  # => enough workers to fetch every page at once
        pages = list(pool.map(fetch_page_sync, range(PAGE_COUNT)))  # => all fetches OVERLAP their I/O waits
    return time.perf_counter() - start, pages  # => elapsed time AND the fetched results


async def run_async_fetch() -> tuple[float, list[int]]:
    start = time.perf_counter()  # => start: wall time before the coroutine-based fetch
    pages = await asyncio.gather(*(fetch_page_async(n) for n in range(PAGE_COUNT)))  # => all sleeps overlap on ONE thread
    return time.perf_counter() - start, list(pages)  # => elapsed time AND the fetched results


def run_process_aggregate() -> int:
    with ProcessPoolExecutor(max_workers=4) as pool:  # => 4 processes -- genuinely parallel CPU work (co-24)
        partial_totals = list(pool.map(sum_of_squares, AGGREGATE_CHUNKS))  # => the "map" phase, in parallel
    return sum(partial_totals)  # => the "reduce" phase -- combining every chunk's partial total (ex-57's pattern)


if __name__ == "__main__":  # => module entry point
    serial_time, serial_pages = run_serial_fetch()  # => serial_time: the fetch baseline
    threaded_time, threaded_pages = run_threaded_fetch()  # => threaded_time: the I/O-overlapping thread-pool fetch
    async_time, async_pages = asyncio.run(run_async_fetch())  # => async_time: the I/O-overlapping asyncio fetch
    process_aggregate = run_process_aggregate()  # => process_aggregate: the CPU-bound reduction, via processes
    serial_aggregate = sum(sum_of_squares(chunk) for chunk in AGGREGATE_CHUNKS)  # => the SERIAL ground truth

    print(f"serial={serial_time:.2f}s threaded={threaded_time:.2f}s async={async_time:.2f}s")  # => Output: serial=~0.36s threaded=~0.06s async=~0.06s

    # => This mini pipeline previews the full capstone's shape (co-01): fetching is I/O-bound, so BOTH
    # => threads (co-23) and `asyncio` (co-26) beat the serial baseline by roughly PAGE_COUNT-fold, since
    # => their I/O waits overlap. Aggregating is CPU-bound, so it instead needs a `ProcessPoolExecutor`
    # => (co-24) to genuinely parallelize across cores -- more threads would NOT have helped there (ex-49,
    # => ex-77). Matching results across every approach, despite their very different execution models,
    # => is the core promise of concurrent programming: SAME correct answer, DIFFERENT wall-clock cost.
    expected_pages = [n * n for n in range(PAGE_COUNT)]  # => expected_pages: the ground-truth fetch result
    assert serial_pages == expected_pages  # => confirms the serial fetch is correct
    assert threaded_pages == expected_pages  # => confirms the threaded fetch is ALSO correct
    assert async_pages == expected_pages  # => confirms the asyncio fetch is ALSO correct
    assert threaded_time < serial_time / 2  # => confirms threads delivered the expected I/O speedup
    assert async_time < serial_time / 2  # => confirms asyncio delivered the expected I/O speedup
    assert process_aggregate == serial_aggregate  # => confirms the parallel aggregate matches the serial one
    print("ex-81 OK")  # => Output: ex-81 OK
