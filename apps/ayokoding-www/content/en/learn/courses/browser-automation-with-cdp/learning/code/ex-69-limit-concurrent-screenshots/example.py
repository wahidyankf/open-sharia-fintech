"""Example 69: reserve only one scarce screenshot-rendering slot."""

import asyncio  # => a semaphore models the rendering resource independently of request count.


# => Two jobs contend for one screenshot slot and observe a peak of one.
async def main() -> int:
    gate, active, maximum = asyncio.Semaphore(1), 0, 0

    async def capture() -> None:
        nonlocal active, maximum
        async with gate:
            active += 1
            maximum = max(maximum, active)
            await asyncio.sleep(0)
            active -= 1

    await asyncio.gather(capture(), capture())
    return maximum


# => The resource-specific cap prevents parallel screenshot work from exhausting the browser.
assert asyncio.run(main()) == 1
# => Output confirms the renderer limit held.
print("maximum concurrent screenshots: 1")
