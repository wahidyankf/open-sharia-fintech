"""Example 7: A Blocking Call Stalls the Loop.

The single most common async bug: a SYNCHRONOUS blocking call inside a coroutine freezes the WHOLE loop,
not just that coroutine. This example proves it, then shows the two correct fixes.
"""

import asyncio  # => the event-loop module (co-02)
import time  # => time.sleep is BLOCKING -- the hazard itself (co-06)


async def good_wait(seconds: float) -> str:  # => the CORRECT async sleep -- yields to the loop
    await asyncio.sleep(seconds)  # => other coroutines keep running during this wait (co-01)
    return "good"


async def bad_wait(seconds: float) -> str:  # => the HAZARD: time.sleep blocks the entire loop (co-06)
    time.sleep(seconds)  # => NO await -- the loop CANNOT switch to any other coroutine while this runs
    return "bad"


async def fixed_wait(seconds: float) -> str:  # => the FIX for genuinely blocking code: offload it (co-06, ex-08)
    loop = asyncio.get_running_loop()  # => fetch the loop this coroutine is running on
    # => run_in_executor pushes the blocking call onto a thread, so the loop stays responsive
    await loop.run_in_executor(None, time.sleep, seconds)  # => the loop is free while the thread blocks
    return "fixed"


async def main() -> dict[str, float]:  # => times BOTH orderings to expose the stall
    start = time.perf_counter()  # => baseline
    await asyncio.gather(bad_wait(0.10), good_wait(0.10))  # => bad blocks good: total ~0.20s, not ~0.10s
    stalled = time.perf_counter() - start  # => the stall made the concurrent pair take the SUM
    # => the fix: offloaded blocking work no longer blocks the loop, so good_wait overlaps it again
    start2 = time.perf_counter()  # => baseline for the fixed run
    await asyncio.gather(fixed_wait(0.10), good_wait(0.10))  # => both run concurrently again
    fixed = time.perf_counter() - start2  # => ~0.10s -- the max, concurrency restored
    return {"stalled": stalled, "fixed": fixed}


if __name__ == "__main__":  # => only runs when executed directly
    times = asyncio.run(main())  # => drive the async main
    print(f"stalled={times['stalled']:.3f}s")  # => Output: stalled=0.20Xs (blocking froze the loop)
    print(f"fixed={times['fixed']:.3f}s")  # => Output: fixed=0.10Xs (offload restored concurrency)
