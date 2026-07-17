"""Example 28: pytest verification for `asyncio.gather` Runs `asyncio.sleep` Tasks Concurrently."""

import asyncio

from example import run_concurrently


def test_gather_overlaps_sleeps_and_preserves_order() -> None:
    labels, total_time = asyncio.run(run_concurrently())
    assert labels == ["a", "b", "c"]  # => order matches the arguments passed to gather()
    assert total_time < 0.4  # => three 0.2s sleeps overlapped, did not sum to 0.6s


# => Run: pytest -- Output: 1 passed
