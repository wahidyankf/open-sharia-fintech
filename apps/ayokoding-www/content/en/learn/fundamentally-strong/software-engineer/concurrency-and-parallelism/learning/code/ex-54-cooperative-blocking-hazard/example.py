"""Example 54: A Blocking `time.sleep` Inside a Coroutine Freezes the ENTIRE Event Loop."""

import asyncio  # => co-26, co-27: cooperative scheduling only works if EVERY coroutine actually cooperates
import time  # => `time.sleep` is a REAL, OS-level blocking call -- the wrong tool inside a coroutine

TICK_INTERVAL = 0.02  # => how often the "ticker" coroutine WOULD like to record a timestamp
TICK_COUNT = 8  # => how many ticks the ticker tries to record, in each scenario


async def blocking_task() -> None:  # => a coroutine that DOES real work the WRONG way
    time.sleep(0.15)  # => BLOCKS the entire OS thread -- the event loop cannot run ANY other coroutine now


async def fixed_task() -> None:  # => the SAME work, done cooperatively
    await asyncio.sleep(0.15)  # => yields control back to the loop -- other coroutines CAN run during this wait


async def ticker(timestamps: list[float]) -> None:
    for _ in range(TICK_COUNT):  # => tries to record TICK_COUNT evenly-spaced timestamps
        timestamps.append(time.perf_counter())  # => records "now" -- reveals whether the loop was stalled
        await asyncio.sleep(TICK_INTERVAL)  # => a COOPERATIVE wait -- lets other coroutines run meanwhile


def max_gap(timestamps: list[float]) -> float:  # => max_gap: the LARGEST delay between consecutive ticks
    gaps = [b - a for a, b in zip(timestamps, timestamps[1:])]  # => gaps: every consecutive tick-to-tick delay
    return max(gaps)  # => a single blocked tick shows up as one unusually LARGE gap


async def run_blocking_scenario() -> list[float]:
    timestamps: list[float] = []  # => timestamps: filled in by the ticker coroutine below
    # => `ticker` is listed FIRST so its Task gets its first scheduling turn BEFORE `blocking_task` --
    # => this lets the ticker record its opening tick, then get frozen mid-run when the block hits,
    # => which is what makes the resulting stall show up AS a gap BETWEEN two of ITS OWN timestamps
    await asyncio.gather(ticker(timestamps), blocking_task())  # => runs BOTH -- but blocking_task starves the ticker
    return timestamps  # => expected to show one big gap where blocking_task hogged the loop


async def run_fixed_scenario() -> list[float]:
    timestamps: list[float] = []  # => timestamps: filled in by the ticker coroutine below
    await asyncio.gather(ticker(timestamps), fixed_task())  # => runs BOTH -- fixed_task cooperates properly
    return timestamps  # => expected to show EVENLY spaced ticks, no starvation gap


if __name__ == "__main__":  # => module entry point
    blocking_gap = max_gap(asyncio.run(run_blocking_scenario()))  # => blocking_gap: the worst stall observed
    fixed_gap = max_gap(asyncio.run(run_fixed_scenario()))  # => fixed_gap: the worst stall in the cooperative version
    print(f"blocking_gap={blocking_gap:.3f}s fixed_gap={fixed_gap:.3f}s")  # => Output: blocking_gap=~0.15s fixed_gap=~0.02s

    # => `time.sleep` inside a coroutine does NOT yield control back to the event loop -- it blocks the
    # => single OS thread the loop runs on, so EVERY other coroutine, including the ticker, is starved
    # => for the entire duration (co-27). Swapping in `await asyncio.sleep(...)` fixes this: it suspends
    # => ONLY the calling coroutine, letting the loop run others in the meantime (co-26). The fix here
    # => generalizes to any accidentally-blocking call inside async code (see ex-55 for the offload fix).
    assert blocking_gap > TICK_INTERVAL * 3  # => confirms the blocking version genuinely starved the ticker
    assert fixed_gap < TICK_INTERVAL * 3  # => confirms the fixed version kept ticking on schedule
    print("ex-54 OK")  # => Output: ex-54 OK
