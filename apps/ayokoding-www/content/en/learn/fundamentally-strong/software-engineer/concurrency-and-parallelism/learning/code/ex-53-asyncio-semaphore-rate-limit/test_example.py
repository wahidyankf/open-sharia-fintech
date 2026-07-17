"""Example 53: pytest verification for `asyncio.Semaphore` Rate Limiting."""

import asyncio

from example import MAX_CONCURRENT, REQUEST_COUNT, run_all


def test_concurrency_never_exceeds_the_semaphore_limit() -> None:
    results, peak = asyncio.run(run_all())
    assert peak <= MAX_CONCURRENT  # => never exceeded the declared cap
    assert peak == MAX_CONCURRENT  # => genuinely reached the cap, not accidentally serialized
    assert results == [n * n for n in range(REQUEST_COUNT)]  # => every request still computed correctly


# => Run: pytest -- Output: 1 passed
