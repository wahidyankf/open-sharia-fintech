"""Example 76: I/O-Bound Work, Benchmarked Three Ways -- Serial vs Threads vs `asyncio`."""

import asyncio  # => co-26: the event-loop approach to concurrent I/O
import time  # => measures wall time across all three approaches
from concurrent.futures import ThreadPoolExecutor  # => co-23: the thread-pool approach

TASK_COUNT = 6  # => how many independent "I/O calls" to make, all THREE ways
SLEEP_SECONDS = 0.08  # => how long each simulated I/O call takes


def sync_io_task(n: int) -> int:  # => n: unused identifier -- only the delay matters
    time.sleep(SLEEP_SECONDS)  # => a blocking I/O simulation -- releases the GIL for real (co-05)
    return n * n  # => trivial result, checkable across all three approaches


async def async_io_task(n: int) -> int:  # => the cooperative-async equivalent of sync_io_task
    await asyncio.sleep(SLEEP_SECONDS)  # => the SAME delay, but yielded cooperatively instead of blocking
    return n * n  # => the identical result-shape as the synchronous version


def run_serial() -> tuple[float, list[int]]:
    start = time.perf_counter()  # => start: wall time before the ONE-AT-A-TIME loop
    results = [sync_io_task(n) for n in range(TASK_COUNT)]  # => runs every call strictly in sequence
    return time.perf_counter() - start, results  # => elapsed time AND the correctness-checkable results


def run_threads() -> tuple[float, list[int]]:
    start = time.perf_counter()  # => start: wall time before the pooled run
    with ThreadPoolExecutor(max_workers=TASK_COUNT) as pool:  # => enough workers to run every task at once
        results = list(pool.map(sync_io_task, range(TASK_COUNT)))  # => all TASK_COUNT calls OVERLAP their sleeps
    return time.perf_counter() - start, results  # => elapsed time AND results


async def run_asyncio() -> tuple[float, list[int]]:
    start = time.perf_counter()  # => start: wall time before the coroutine-based run
    results = await asyncio.gather(*(async_io_task(n) for n in range(TASK_COUNT)))  # => all sleeps overlap on ONE thread
    return time.perf_counter() - start, list(results)  # => elapsed time AND results


if __name__ == "__main__":  # => module entry point
    serial_time, serial_results = run_serial()  # => serial_time: the single-threaded baseline
    threads_time, threads_results = run_threads()  # => threads_time: the multi-threaded, I/O-overlapping run
    asyncio_time, asyncio_results = asyncio.run(run_asyncio())  # => asyncio_time: the single-threaded, cooperative run

    print(f"serial={serial_time:.2f}s threads={threads_time:.2f}s asyncio={asyncio_time:.2f}s")
    # => Output: serial=~0.48s threads=~0.08s asyncio=~0.08s

    expected = [n * n for n in range(TASK_COUNT)]  # => expected: the ground-truth result, identical across all three

    # => I/O-bound work is where BOTH concurrency models genuinely help (co-05): threads overlap their
    # => blocking `time.sleep` calls because each one releases the GIL while waiting (co-23), and
    # => `asyncio` overlaps its cooperative `await asyncio.sleep` calls on a SINGLE thread via the event
    # => loop (co-26). Both beat the serial baseline by roughly TASK_COUNT-fold here, because the total
    # => wall time collapses to about ONE task's duration instead of the sum of every task's duration.
    assert threads_time < serial_time / 2  # => confirms threads delivered a substantial I/O speedup
    assert asyncio_time < serial_time / 2  # => confirms asyncio ALSO delivered a substantial I/O speedup
    assert serial_results == expected  # => confirms the serial run's results are correct
    assert threads_results == expected  # => confirms the threaded run's results are ALSO correct
    assert asyncio_results == expected  # => confirms the asyncio run's results are ALSO correct
    print("ex-76 OK")  # => Output: ex-76 OK
