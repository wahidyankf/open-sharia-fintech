"""Example 8: Offloading Blocking Work to an Executor."""

import asyncio  # => the event-loop module (co-02)
import time  # => only to simulate + measure


def blocking_cpu_or_io(seconds: float) -> int:  # => a PLAIN synchronous function -- NOT a coroutine
    # => imagine a blocking DB driver, a CPU-heavy computation, or a C-extension call (co-06)
    time.sleep(seconds)  # => blocks the THREAD it runs on -- fine on a pool thread, fatal on the loop
    return 42  # => a plain return value, handed back across the executor boundary


async def main() -> tuple[int, float]:  # => keeps the loop responsive while a thread does the blocking work
    loop = asyncio.get_running_loop()  # => the loop this coroutine is running on
    start = time.perf_counter()  # => baseline
    # => run_in_executor schedules the blocking function on a thread pool, returning an awaitable (co-03, co-06)
    # => the FIRST arg is the executor (None = the default ThreadPoolExecutor); the loop stays free meanwhile
    result = await loop.run_in_executor(None, blocking_cpu_or_io, 0.10)  # => awaited -> resolves to the int
    # => a SECOND coroutine scheduled alongside would keep running during that 0.10s (co-02) -- the win
    elapsed = time.perf_counter() - start  # => ~0.10s on the thread, with the loop still responsive
    return result, elapsed


if __name__ == "__main__":  # => only runs when executed directly
    result, elapsed = asyncio.run(main())  # => drive the async main
    print(result)  # => Output: 42
    print(f"elapsed={elapsed:.3f}s")  # => Output: elapsed=0.10Xs (loop never stalled)
