"""Example 50: pytest verification for `asyncio.create_task` Concurrent Scheduling."""

import asyncio

from example import main


def test_create_task_overlaps_while_sequential_await_does_not() -> None:
    sequential_time, concurrent_time, sequential_results, concurrent_results = asyncio.run(main())
    assert concurrent_time < sequential_time / 2  # => create_task delivered genuine overlap
    assert sequential_results == concurrent_results  # => both computed the identical results


# => Run: pytest -- Output: 1 passed
