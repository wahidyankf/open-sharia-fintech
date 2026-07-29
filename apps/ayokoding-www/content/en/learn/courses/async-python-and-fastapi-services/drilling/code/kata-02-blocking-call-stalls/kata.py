"""Kata 2 -- Prove a blocking call stalls the loop (co-06)."""

import asyncio  # => co-06: blocking stalls the loop
import time


async def good(d: float) -> None:  # => an async wait
    await asyncio.sleep(d)  # => yields


async def blocker(d: float) -> None:  # => a BLOCKING wait -- the hazard (co-06)
    time.sleep(d)  # => NO await -> freezes the whole loop


async def fixed(
    d: float,
) -> None:  # => offloaded blocking -> loop stays responsive (co-06, co-03)
    loop = asyncio.get_running_loop()  # => the running loop
    await loop.run_in_executor(None, time.sleep, d)  # => blocking runs on a thread


async def run_with_blocker(
    d: float,
) -> float:  # => gather bad + good -> ~2d (bad froze good)
    start = time.perf_counter()
    await asyncio.gather(blocker(d), good(d))  # => bad blocks good
    return time.perf_counter() - start


async def run_fixed(
    d: float,
) -> float:  # => gather fixed + good -> ~d (concurrency restored)
    start = time.perf_counter()
    await asyncio.gather(fixed(d), good(d))  # => both run concurrently again
    return time.perf_counter() - start


def main() -> None:
    stalled = asyncio.run(run_with_blocker(0.10))  # => ~0.2 -- the stall
    ok = asyncio.run(run_fixed(0.10))  # => ~0.1 -- fixed
    print(f"stalled={stalled:.3f}s fixed={ok:.3f}s")
    assert ok < stalled  # => the offload restored concurrency


if __name__ == "__main__":
    main()
