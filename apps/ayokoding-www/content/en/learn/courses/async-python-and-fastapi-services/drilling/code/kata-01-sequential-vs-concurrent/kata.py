"""Kata 1 -- Time two awaits sequentially vs. concurrently (co-04)."""

import asyncio  # => co-04: gather runs the waits concurrently
import time


async def pause(seconds: float) -> None:  # => a unit of async work
    await asyncio.sleep(seconds)  # => yields to the loop (co-01)


async def measure_sequential(d: float) -> float:  # => two awaits IN SEQUENCE -> ~2d
    start = time.perf_counter()  # => baseline
    await pause(d)  # => first wait
    await pause(d)  # => second wait, stacked after the first
    return time.perf_counter() - start  # => ~2d


async def measure_concurrent(d: float) -> float:  # => gather -> ~d
    start = time.perf_counter()  # => baseline
    await asyncio.gather(
        pause(d), pause(d)
    )  # => both run concurrently on one loop (co-04)
    return time.perf_counter() - start  # => ~d -- the max, not the sum


def main() -> None:  # => drives both measurements
    seq = asyncio.run(measure_sequential(0.10))  # => sequential
    con = asyncio.run(measure_concurrent(0.10))  # => concurrent
    print(
        f"sequential={seq:.3f}s concurrent={con:.3f}s"
    )  # => sequential ~0.2, concurrent ~0.1
    assert con < seq  # => concurrency is genuinely faster here


if __name__ == "__main__":
    main()
