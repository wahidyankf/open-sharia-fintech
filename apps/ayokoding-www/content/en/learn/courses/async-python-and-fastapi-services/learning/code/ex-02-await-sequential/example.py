"""Example 2: Sequential Awaits Add Up."""

import asyncio  # => the event-loop module (co-02)
import time  # => only to MEASURE wall-clock time, never to "sleep" inside a coroutine (see ex-07)


async def pause(seconds: float) -> str:  # => a coroutine that simply waits, then returns a label
    # => await yields to the loop for the given duration -- other coroutines could run meanwhile (co-01)
    await asyncio.sleep(seconds)  # => the awaitable here is asyncio.sleep's coroutine
    return f"paused {seconds}s"  # => returned to whoever awaits this coroutine


async def main() -> tuple[str, str, float]:  # => two awaits IN SEQUENCE -- the second starts after the first ends
    start = time.perf_counter()  # => capture start time BEFORE the first await
    first = await pause(0.10)  # => awaited alone: the loop waits ~0.10s, doing nothing else here
    # => only AFTER first completes does the second await even begin -- they are SERIAL
    second = await pause(0.10)  # => a second ~0.10s wait, stacked after the first
    elapsed = time.perf_counter() - start  # => total wall-clock cost of BOTH waits
    # => elapsed is ~0.20s -- the SUM, because nothing ran concurrently (contrast ex-03)
    return first, second, elapsed


if __name__ == "__main__":  # => only runs when executed directly
    f, s, elapsed = asyncio.run(main())  # => drive the async main with a fresh loop
    print(f)  # => Output: paused 0.1s
    print(s)  # => Output: paused 0.1s
    print(f"elapsed={elapsed:.3f}s")  # => Output: elapsed=0.20Xs (the sum of both waits)
