"""Example 28: `asyncio.gather` Runs `asyncio.sleep` Tasks Concurrently."""

import asyncio  # => co-26's event loop, plus co-05: I/O-bound work benefits from concurrency
import time  # => measures wall time to prove the sleeps genuinely overlapped


async def wait_and_return(label: str, delay: float) -> str:  # => one "I/O-bound" coroutine
    await asyncio.sleep(delay)  # => suspends THIS coroutine -- the event loop runs OTHERS meanwhile
    return label  # => returned once this coroutine resumes after its own delay elapses


async def run_concurrently() -> tuple[list[str], float]:  # => runs 3 sleeps AT THE SAME TIME
    start = time.perf_counter()  # => start: wall time before any coroutine begins awaiting
    results = await asyncio.gather(  # => schedules all three coroutines on the SAME event loop
        wait_and_return("a", 0.2),  # => sleeps 0.2s
        wait_and_return("b", 0.2),  # => ALSO sleeps 0.2s -- concurrently with "a", not after it
        wait_and_return("c", 0.2),  # => ALSO sleeps 0.2s -- all three overlap on one thread
    )
    elapsed = time.perf_counter() - start  # => elapsed: close to 0.2s total, NOT 0.6s
    return list(results), elapsed  # => results preserve gather()'s input ORDER, regardless of timing


if __name__ == "__main__":  # => module entry point
    labels, total_time = asyncio.run(run_concurrently())  # => drives the whole gather() to completion
    print(labels)  # => Output: ['a', 'b', 'c']
    print(f"total_time={total_time:.2f}s")  # => Output: total_time=~0.2s

    # => `asyncio.gather` schedules every coroutine passed to it on the SAME single-threaded event
    # => loop -- while one is suspended in `await asyncio.sleep(...)`, the loop runs another. Three
    # => 0.2s sleeps therefore finish in ~0.2s total, not 0.6s, exactly like ex-05's threaded version.
    assert labels == ["a", "b", "c"]  # => confirms gather() preserves the ORIGINAL argument order
    assert total_time < 0.4  # => confirms the three sleeps overlapped instead of running sequentially
    print("ex-28 OK")  # => Output: ex-28 OK
