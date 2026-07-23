"""Example 23: pytest verification for `ThreadPoolExecutor.map` Over I/O Tasks."""

import time
from concurrent.futures import ThreadPoolExecutor

from example import fetch


def test_map_returns_results_in_input_order_and_overlaps() -> None:
    ids = [10, 20, 30, 40]
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, ids))
    elapsed = time.perf_counter() - start
    assert results == [f"result-{i}" for i in ids]  # => order matches input, not finish time
    assert elapsed < 0.3  # => 4 fetches overlapped, did not run serially (would be ~0.4s)


# => Run: pytest -- Output: 1 passed
