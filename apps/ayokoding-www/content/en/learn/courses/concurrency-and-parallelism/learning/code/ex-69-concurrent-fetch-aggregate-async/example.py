"""Example 69: Fetch Many "URLs" Concurrently, Rate-Limited, Then Aggregate."""

import asyncio  # => co-26, co-13: gather for aggregation, a Semaphore for the rate limit

URLS = [f"https://example.test/page-{i}" for i in range(12)]  # => URLS: 12 simulated pages to "fetch"
MAX_CONCURRENT_FETCHES = 3  # => at most this many "requests" may be in flight simultaneously


async def fetch_page(url: str, sem: asyncio.Semaphore, active: list[int], peak: list[int]) -> int:
    async with sem:  # => throttles concurrency -- the SAME pattern as ex-53, applied to a real-shaped task
        active[0] += 1  # => one more fetch now "in flight"
        peak[0] = max(peak[0], active[0])  # => peak: the highest concurrency level EVER observed
        await asyncio.sleep(0.02)  # => simulates network latency -- a REAL fetch would `await` here too
        active[0] -= 1  # => this fetch is done -- frees a permit for the next waiter
        return len(url)  # => stands in for "content length" -- a trivial but checkable per-page result


async def fetch_and_aggregate() -> tuple[int, int]:
    sem = asyncio.Semaphore(MAX_CONCURRENT_FETCHES)  # => sem: the shared limiter for all 12 fetches
    active = [0]  # => active[0]: how many fetches are CURRENTLY in flight
    peak = [0]  # => peak[0]: updated inside every fetch -- the maximum concurrency actually reached
    lengths = await asyncio.gather(*(fetch_page(url, sem, active, peak) for url in URLS))  # => runs ALL 12 concurrently
    total_length = sum(lengths)  # => total_length: the AGGREGATE across every fetched page
    return total_length, peak[0]  # => everything the caller needs to verify correctness AND the rate limit


if __name__ == "__main__":  # => module entry point
    total_length, peak = asyncio.run(fetch_and_aggregate())  # => drives all 12 fetches through the shared semaphore
    print(f"total_length={total_length} peak={peak}")  # => Output: total_length=<sum of URL lengths> peak=3

    expected_total = sum(len(url) for url in URLS)  # => expected_total: the serial, ground-truth aggregate

    # => Fetching many resources concurrently AND aggregating their results is one of `asyncio.gather`'s
    # => most common real-world uses (co-26) -- but unbounded concurrency can overwhelm the target
    # => server (or a rate-limited API). Wrapping each fetch in `async with sem:` (co-13, exactly as in
    # => ex-53) caps how many are in flight at once WITHOUT changing the aggregation logic at all: the
    # => `gather()` call still collects every result, in order, once all 12 fetches have completed.
    assert total_length == expected_total  # => confirms the aggregate exactly matches the serial baseline
    assert peak <= MAX_CONCURRENT_FETCHES  # => confirms concurrency NEVER exceeded the declared cap
    assert peak == MAX_CONCURRENT_FETCHES  # => confirms concurrency actually REACHED the cap -- genuinely throttled
    print("ex-69 OK")  # => Output: ex-69 OK
