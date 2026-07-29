"""Example 3: Concurrent Awaits with gather."""

import asyncio  # => the event-loop module -- gather lives here (co-04)
import time  # => wall-clock measurement only


async def pause(seconds: float) -> str:  # => the SAME coroutine as ex-02
    await asyncio.sleep(seconds)  # => yields to the loop for the given duration (co-01)
    return f"paused {seconds}s"  # => labelled result


async def main() -> tuple[list[str], float]:  # => results come back IN ORDER, time is the MAX
    start = time.perf_counter()  # => capture start before fanning out
    # => asyncio.gather SCHEDULES both coroutines concurrently and waits for ALL of them (co-04)
    # => the loop interleaves the two waits, so they overlap instead of stacking
    results = await asyncio.gather(pause(0.10), pause(0.10))  # => returns a list, order preserved
    elapsed = time.perf_counter() - start  # => total cost is ~the SLOWER call, not the sum
    # => contrast ex-02's ~0.20s: same two waits, but ~0.10s here -- the concurrency win (co-04)
    return results, elapsed


if __name__ == "__main__":  # => only runs when executed directly
    results, elapsed = asyncio.run(main())  # => drive the async main
    print(results)  # => Output: ['paused 0.1s', 'paused 0.1s']
    print(f"elapsed={elapsed:.3f}s")  # => Output: elapsed=0.10Xs (the max, not the sum)
