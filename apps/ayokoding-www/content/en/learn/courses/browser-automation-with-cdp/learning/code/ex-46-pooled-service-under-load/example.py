"""Example 46: a bounded local service stays within its page-pool capacity."""

import asyncio  # => asyncio lets callers overlap while the semaphore enforces the resource limit.


# => Three callers share two slots, so the observed maximum must never exceed two.
async def main() -> int:
    gate, active, maximum = asyncio.Semaphore(2), 0, 0

    async def request() -> None:
        nonlocal active, maximum
        async with gate:
            active += 1
            maximum = max(maximum, active)
            await asyncio.sleep(0)
            active -= 1

    await asyncio.gather(*(request() for _ in range(3)))
    return maximum


# => Capacity is an assertion, not merely a configuration claim.
assert asyncio.run(main()) == 2
# => Output reports the pool contract held under concurrent clients.
print("service peak concurrency: 2")
