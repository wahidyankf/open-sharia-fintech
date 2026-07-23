"""Example 50: `asyncio.create_task` Schedules Work CONCURRENTLY, Not Sequentially."""

import asyncio  # => co-26: the single-threaded, cooperative event loop model
import time  # => measures wall time to prove concurrent overlap vs plain sequential awaiting

DELAY = 0.1  # => how long each simulated "I/O wait" coroutine takes
TASK_COUNT = 5  # => how many independent coroutines to run both ways


async def wait_a_bit(n: int) -> int:  # => a coroutine -- suspends cooperatively, does NOT block the loop
    await asyncio.sleep(DELAY)  # => await asyncio.sleep(): yields control back to the event loop while "waiting"
    return n * n  # => a trivial result so the caller has something to check


async def sequential_awaits() -> list[int]:
    results: list[int] = []  # => results: collected one at a time, each `await` blocking THIS coroutine's progress
    for n in range(TASK_COUNT):  # => awaits each coroutine to FULLY complete before starting the next
        results.append(await wait_a_bit(n))  # => the next iteration doesn't even START until this one finishes
    return results  # => took roughly TASK_COUNT * DELAY seconds in total


async def concurrent_via_create_task() -> list[int]:
    tasks = [asyncio.create_task(wait_a_bit(n)) for n in range(TASK_COUNT)]
    # => create_task SCHEDULES the coroutine to start running on the NEXT event-loop iteration -- doesn't wait
    results = [await t for t in tasks]  # => NOW awaits each Task -- but they were ALREADY running concurrently
    return results  # => took roughly ONE DELAY in total, since all 5 sleeps overlapped


async def main() -> tuple[float, float, list[int], list[int]]:
    start_sequential = time.perf_counter()  # => start_sequential: wall time before the strictly sequential run
    sequential_results = await sequential_awaits()  # => runs all 5 coroutines one after another
    sequential_time = time.perf_counter() - start_sequential  # => sequential_time: roughly TASK_COUNT * DELAY

    start_concurrent = time.perf_counter()  # => start_concurrent: wall time before the create_task-based run
    concurrent_results = await concurrent_via_create_task()  # => runs all 5 coroutines with their sleeps OVERLAPPING
    concurrent_time = time.perf_counter() - start_concurrent  # => concurrent_time: roughly ONE DELAY, not 5

    return sequential_time, concurrent_time, sequential_results, concurrent_results  # => everything the caller needs


if __name__ == "__main__":  # => module entry point
    sequential_time, concurrent_time, sequential_results, concurrent_results = asyncio.run(main())
    print(f"sequential={sequential_time:.2f}s concurrent={concurrent_time:.2f}s")  # => Output: sequential=~0.50s concurrent=~0.10s

    # => `await coroutine()` directly runs that coroutine to completion before moving on -- it does NOT
    # => introduce concurrency by itself. `asyncio.create_task(coroutine())` is what actually SCHEDULES a
    # => coroutine to start running independently, letting multiple coroutines' `await asyncio.sleep(...)`
    # => calls overlap in wall-clock time (co-26). Awaiting the Tasks afterward just collects results that
    # => were, in many cases, ALREADY computed concurrently -- the scheduling happened at create_task time.
    assert concurrent_time < sequential_time / 2  # => confirms create_task delivered genuine overlap, not just syntax
    assert sequential_results == concurrent_results  # => confirms both approaches computed the identical results
    print("ex-50 OK")  # => Output: ex-50 OK
