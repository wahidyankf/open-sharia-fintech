"""Example 23: `ThreadPoolExecutor.map` Over I/O Tasks."""

import time  # => simulates I/O latency with `time.sleep`, as in ex-05
from concurrent.futures import ThreadPoolExecutor  # => co-23: a reusable pool of worker threads


def fetch(item_id: int) -> str:  # => stands in for a network/disk call keyed by `item_id`
    time.sleep(0.1)  # => simulated I/O latency -- releases the GIL, just like ex-05's fake_io_call
    return f"result-{item_id}"  # => a deterministic, checkable "response" for this id


if __name__ == "__main__":  # => module entry point
    ids = [1, 2, 3, 4, 5]  # => 5 independent "requests" to fetch concurrently
    start = time.perf_counter()  # => start: wall-clock time before the pool does any work
    with ThreadPoolExecutor(max_workers=5) as pool:  # => 5 reusable worker threads, auto-shutdown on exit
        results = list(pool.map(fetch, ids))  # => map() applies fetch() to each id, IN ORDER, concurrently
    elapsed = time.perf_counter() - start  # => elapsed: total wall time for all 5 fetches combined

    print(results)  # => Output: ['result-1', 'result-2', 'result-3', 'result-4', 'result-5']
    print(f"elapsed={elapsed:.2f}s")  # => Output: elapsed=~0.1s (NOT ~0.5s -- proves overlap)

    # => `.map()` guarantees results come back in the SAME order as the input iterable, even
    # => though the underlying fetch() calls may finish in any order across the worker threads.
    assert results == [f"result-{i}" for i in ids]  # => confirms order matches input, not completion time
    assert elapsed < 0.3  # => confirms the 5 fetches overlapped instead of running one after another
    print("ex-23 OK")  # => Output: ex-23 OK
