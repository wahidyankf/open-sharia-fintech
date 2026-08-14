"""Example 35: a semaphore bounds concurrent fixture page work."""

import asyncio  # => semaphore ownership models scarce browser-target capacity.


# => Track the greatest simultaneous workload while a two-slot pool runs three jobs.
async def main() -> int:
    gate, active, maximum = asyncio.Semaphore(2), 0, 0

    async def work() -> None:
        nonlocal active, maximum
        async with gate:
            active += 1
            maximum = max(maximum, active)
            await asyncio.sleep(0)
            active -= 1

    await asyncio.gather(*(work() for _ in range(3)))
    return maximum


# => The assertion is the pool contract: capacity never exceeds two active targets.
assert asyncio.run(main()) == 2
# => Output confirms the resource cap held under concurrent callers.
print("maximum concurrent pages: 2")
