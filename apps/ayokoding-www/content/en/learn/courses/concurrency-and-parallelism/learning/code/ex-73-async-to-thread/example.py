"""Example 73: `asyncio.to_thread` -- the High-Level Shortcut for Offloading Blocking Calls."""

import asyncio  # => co-27, co-23: `asyncio.to_thread` (3.9+) wraps `run_in_executor` in a friendlier API
import time  # => simulates a blocking call with no async equivalent

TICK_INTERVAL = 0.02  # => how often the ticker coroutine records a timestamp
TICK_COUNT = 8  # => how many ticks the ticker tries to record


def blocking_legacy_call(delay: float) -> str:  # => a PLAIN (non-async) function -- imagine a sync SDK call
    time.sleep(delay)  # => genuinely blocks the calling thread -- this is the whole point of the example
    return "legacy result"  # => the result this blocking call eventually produces


async def ticker(timestamps: list[float]) -> None:
    for _ in range(TICK_COUNT):  # => tries to record TICK_COUNT evenly-spaced timestamps
        timestamps.append(time.perf_counter())  # => records "now" -- reveals whether the loop stayed responsive
        await asyncio.sleep(TICK_INTERVAL)  # => a cooperative wait, letting other coroutines/tasks run


def max_gap(timestamps: list[float]) -> float:  # => max_gap: the LARGEST delay between consecutive ticks
    gaps = [b - a for a, b in zip(timestamps, timestamps[1:])]  # => gaps: every consecutive tick-to-tick delay
    return max(gaps)  # => a stalled loop shows up as one unusually LARGE gap


async def run_with_to_thread() -> tuple[list[float], str]:
    timestamps: list[float] = []  # => timestamps: filled in by the ticker coroutine below
    offloaded = asyncio.to_thread(blocking_legacy_call, 0.15)  # => `to_thread` == `run_in_executor(None, func, *args)`
    result, _ = await asyncio.gather(offloaded, ticker(timestamps))  # => runs BOTH concurrently, offloaded first
    return timestamps, result  # => everything the caller needs to verify responsiveness AND correctness


if __name__ == "__main__":  # => module entry point
    timestamps, result = asyncio.run(run_with_to_thread())  # => drives the offloaded scenario to completion
    gap = max_gap(timestamps)  # => gap: the worst stall the ticker actually observed
    print(f"gap={gap:.3f}s result={result!r}")  # => Output: gap=~0.02s result='legacy result'

    # => `asyncio.to_thread(func, *args)` is sugar for `loop.run_in_executor(None, func, *args)` (ex-55) --
    # => same underlying mechanism (a background thread from the loop's default `ThreadPoolExecutor`,
    # => co-23), but without needing to fetch the running loop explicitly first (co-27). Prefer
    # => `to_thread` in ordinary async code; reach for the lower-level `run_in_executor` only when you
    # => need a NON-default executor (e.g. a `ProcessPoolExecutor` for CPU-bound offloaded work).
    assert gap < TICK_INTERVAL * 3  # => confirms the ticker stayed on schedule -- the loop was NEVER stalled
    assert result == "legacy result"  # => confirms the offloaded call still produced the correct result
    print("ex-73 OK")  # => Output: ex-73 OK
