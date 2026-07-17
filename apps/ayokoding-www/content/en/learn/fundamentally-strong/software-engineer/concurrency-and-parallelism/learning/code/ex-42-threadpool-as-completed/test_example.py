"""Example 42: pytest verification for `as_completed` Finish-Order Delivery."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from example import slow_task


def test_as_completed_yields_the_fastest_task_first() -> None:
    delays = [0.1, 0.01, 0.05]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(slow_task, i, d) for i, d in enumerate(delays)]
        order: list[int] = [f.result()[0] for f in as_completed(futures)]
    assert order[0] == 1  # => task 1 has the shortest delay -- it must be the first to complete
    assert set(order) == {0, 1, 2}  # => every task still completes, just not in submit order


# => Run: pytest -- Output: 1 passed
