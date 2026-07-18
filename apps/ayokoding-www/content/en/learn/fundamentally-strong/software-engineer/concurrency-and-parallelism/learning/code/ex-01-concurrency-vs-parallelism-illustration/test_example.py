"""Example 1: pytest verification for Concurrency vs. Parallelism, Illustrated."""

import asyncio

from example import concurrency_demo, parallelism_demo


def test_coroutines_interleave_on_one_thread() -> None:
    # => two coroutines sharing one thread must ALTERNATE, never run "at once"
    log: list[str] = asyncio.run(concurrency_demo())
    assert log == ["A0", "B0", "A1", "B1", "A2", "B2"]  # => strict interleave order


def test_two_processes_overlap_in_wall_time() -> None:
    # => two 0.3s CPU-bound processes should finish close to 0.3s, not 0.6s, if truly parallel
    elapsed = parallelism_demo()
    assert elapsed < 0.6  # => generous margin: proves overlap without depending on exact timing


# => Run: pytest -- Output: 2 passed
