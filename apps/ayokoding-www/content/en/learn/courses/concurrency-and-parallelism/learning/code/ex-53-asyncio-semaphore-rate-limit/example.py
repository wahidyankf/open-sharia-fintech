"""Example 53: `asyncio.Semaphore` Caps How Many Coroutines Run "In Flight" at Once."""

import asyncio  # => co-26, co-13: the async counterpart to ex-15's threaded Semaphore

MAX_CONCURRENT = 3  # => at most this many "requests" may be in flight simultaneously
REQUEST_COUNT = 10  # => far more requests than MAX_CONCURRENT -- forces genuine queuing


async def limited_request(sem: asyncio.Semaphore, n: int, active: list[int], peak: list[int]) -> int:
    async with sem:  # => `await`s until a permit is free -- blocks THIS coroutine, not the whole loop
        active[0] += 1  # => one more request is now "in flight"
        peak[0] = max(peak[0], active[0])  # => peak: the highest concurrency level EVER observed
        await asyncio.sleep(0.02)  # => simulates the request's own work, while HOLDING the semaphore
        active[0] -= 1  # => this request is done -- frees up a permit for the next waiter
        return n * n  # => a trivial "response" so the caller has something to verify


async def run_all() -> tuple[list[int], int]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)  # => sem: the shared limiter, permitting MAX_CONCURRENT holders
    active = [0]  # => active[0]: how many `limited_request` calls are CURRENTLY inside the semaphore
    peak = [0]  # => peak[0]: updated inside every call -- the maximum concurrency actually reached
    results = await asyncio.gather(*(limited_request(sem, n, active, peak) for n in range(REQUEST_COUNT)))
    return list(results), peak[0]  # => results: every response, in submission order; peak[0]: the max observed


if __name__ == "__main__":  # => module entry point
    results, peak = asyncio.run(run_all())  # => drives all REQUEST_COUNT requests through the shared semaphore
    print(f"results={results} peak={peak}")  # => Output: results=[0, 1, 4, ..., 81] peak=3

    # => `asyncio.Semaphore` works exactly like `threading.Semaphore` (ex-15) conceptually -- it caps how
    # => many "holders" may be inside the `async with sem:` block at once -- but its `acquire`/`release`
    # => are cooperative `await` points rather than OS-level blocking calls (co-26). This is the standard
    # => way to rate-limit concurrent requests (to an API, a database, a rate-limited service) from
    # => async code: launch as MANY coroutines as you want, and let the semaphore throttle concurrency.
    assert peak <= MAX_CONCURRENT  # => confirms concurrency NEVER exceeded the semaphore's declared limit
    assert peak == MAX_CONCURRENT  # => confirms concurrency actually REACHED the limit -- genuinely throttled, not accidental
    assert results == [n * n for n in range(REQUEST_COUNT)]  # => confirms every request still got the right answer
    print("ex-53 OK")  # => Output: ex-53 OK
