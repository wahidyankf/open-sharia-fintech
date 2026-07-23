"""Example 55: `loop.run_in_executor` -- Offloading a TRULY Blocking Call Off the Event Loop."""

import asyncio  # => co-27: for calls that CANNOT be made cooperative (no async version exists)
import time  # => simulates a blocking call with no async equivalent -- e.g. a legacy C-extension or sync SDK

TICK_INTERVAL = 0.02  # => how often the ticker coroutine records a timestamp
TICK_COUNT = 8  # => how many ticks the ticker records


def blocking_legacy_call(delay: float) -> str:  # => a PLAIN (non-async) function -- simulates unavoidable blocking I/O
    time.sleep(delay)  # => genuinely blocks the calling thread -- imagine this is a legacy synchronous SDK call
    return "legacy result"  # => the result this blocking call eventually produces


async def ticker(timestamps: list[float]) -> None:
    for _ in range(TICK_COUNT):  # => tries to record TICK_COUNT evenly-spaced timestamps
        timestamps.append(time.perf_counter())  # => records "now" -- reveals whether the loop stayed responsive
        await asyncio.sleep(TICK_INTERVAL)  # => a cooperative wait, letting other coroutines/tasks run


def max_gap(timestamps: list[float]) -> float:  # => max_gap: the LARGEST delay between consecutive ticks
    gaps = [b - a for a, b in zip(timestamps, timestamps[1:])]  # => gaps: every consecutive tick-to-tick delay
    return max(gaps)  # => a stalled loop shows up as one unusually LARGE gap


async def run_offloaded() -> tuple[list[float], str]:
    loop = asyncio.get_running_loop()  # => loop: the CURRENTLY running event loop, needed to schedule the offload
    timestamps: list[float] = []  # => timestamps: filled in by the ticker coroutine below
    offloaded_call = loop.run_in_executor(None, blocking_legacy_call, 0.15)  # => runs on a background THREAD, not the loop
    # => `None` as the executor means "use the loop's default ThreadPoolExecutor" -- co-23 under the hood
    ticker_call = ticker(timestamps)  # => ticker_call: the SAME cooperative ticker coroutine as ex-54
    _, legacy_result = await asyncio.gather(ticker_call, offloaded_call)  # => awaits BOTH concurrently
    return timestamps, legacy_result  # => everything the caller needs to verify responsiveness AND correctness


if __name__ == "__main__":  # => module entry point
    timestamps, legacy_result = asyncio.run(run_offloaded())  # => drives the offloaded scenario to completion
    gap = max_gap(timestamps)  # => gap: the worst stall the ticker actually observed
    print(f"gap={gap:.3f}s legacy_result={legacy_result!r}")  # => Output: gap=~0.02s legacy_result='legacy result'

    # => `loop.run_in_executor(None, func, *args)` runs a genuinely BLOCKING, non-async function on a
    # => background thread from the loop's default `ThreadPoolExecutor` (co-23), and returns an
    # => awaitable that resolves once that thread's call completes -- WITHOUT blocking the event loop
    # => itself. This is the correct fix (co-27) when the blocking call has no async equivalent to swap
    # => in (contrast ex-54, where `time.sleep` COULD simply become `asyncio.sleep`): the event loop
    # => keeps servicing other coroutines (like the ticker here) the entire time the thread is blocked.
    assert gap < TICK_INTERVAL * 3  # => confirms the ticker stayed on schedule -- the loop was NEVER stalled
    assert legacy_result == "legacy result"  # => confirms the offloaded call still produced the correct result
    print("ex-55 OK")  # => Output: ex-55 OK
