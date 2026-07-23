"""Example 69: pytest verification for Concurrent Fetch + Aggregate with a Semaphore Cap."""

import asyncio

from example import MAX_CONCURRENT_FETCHES, URLS, fetch_and_aggregate


def test_aggregate_correct_and_concurrency_capped() -> None:
    total_length, peak = asyncio.run(fetch_and_aggregate())
    expected_total = sum(len(url) for url in URLS)
    assert total_length == expected_total  # => the aggregate exactly matches the serial baseline
    assert peak <= MAX_CONCURRENT_FETCHES  # => concurrency never exceeded the declared cap
    assert peak == MAX_CONCURRENT_FETCHES  # => concurrency actually reached the cap


# => Run: pytest -- Output: 1 passed
