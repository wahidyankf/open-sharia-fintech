"""Example 1: Concurrency vs. Parallelism, Illustrated."""  # => co-01: interleaving one thing at a time vs truly simultaneous

import asyncio  # => single-threaded cooperative concurrency (co-01)
import multiprocessing as mp  # => true OS-level parallelism, separate processes (co-01)
import time  # => used to measure wall-clock overlap for the parallelism half


async def worker(name: str, steps: int, log: list[str]) -> None:  # => one "concurrent" task
    for i in range(steps):  # => each task takes several small steps
        log.append(f"{name}{i}")  # => records the step BEFORE yielding control
        await asyncio.sleep(0)  # => yields to the event loop -- co-27's "voluntary" handoff
        # => control may now run the OTHER task's next step before this one resumes


async def concurrency_demo() -> list[str]:  # => runs two coroutines on ONE thread
    log: list[str] = []  # => shared list -- both coroutines append to it, in whatever order runs
    await asyncio.gather(  # => schedules BOTH coroutines on the same event loop
        worker("A", 3, log),  # => task A: 3 steps
        worker("B", 3, log),  # => task B: 3 steps -- interleaves with A, never truly simultaneous
    )  # => gather() returns once BOTH coroutines have fully completed
    return log  # => an INTERLEAVED sequence: A0, B0, A1, B1, ... (order proves cooperative handoff)


def cpu_burn(seconds: float) -> None:  # => a process-local CPU-bound loop (used for parallelism)
    end = time.monotonic() + seconds  # => end is a wall-clock deadline this loop runs until
    total = 0  # => a throwaway accumulator -- forces real CPU work, not an idle sleep
    while time.monotonic() < end:  # => keeps looping until the deadline passes
        total += 1  # => pure CPU work, no I/O -- this is what a THREAD cannot parallelize (co-03)
    _ = total  # => silences "unused variable" -- the loop's side effect (time spent) is the point


def parallelism_demo() -> float:  # => runs two OS processes SIMULTANEOUSLY on separate cores
    duration = 0.3  # => each process burns CPU for this many seconds
    start = time.monotonic()  # => start is the wall-clock time before either process launches
    procs = [mp.Process(target=cpu_burn, args=(duration,)) for _ in range(2)]  # => two child processes
    for p in procs:  # => launches both -- each gets its OWN interpreter, OWN GIL (co-02)
        p.start()  # => start() forks/spawns a real OS process, not a lightweight thread
    for p in procs:  # => waits for both to finish
        p.join()  # => join() blocks until that specific process exits
    elapsed = time.monotonic() - start  # => elapsed is the WALL-CLOCK time for BOTH combined
    return elapsed  # => if truly parallel, elapsed is close to `duration`, not `2 * duration`


if __name__ == "__main__":  # => required on macOS/Windows: multiprocessing re-imports this module
    interleaved_log = asyncio.run(concurrency_demo())  # => runs the coroutine demo to completion
    print(interleaved_log)  # => Output: ['A0', 'B0', 'A1', 'B1', 'A2', 'B2']

    parallel_elapsed = parallelism_demo()  # => runs the two-process demo, returns wall time
    print(f"parallel_elapsed < 0.6s: {parallel_elapsed < 0.6}")  # => Output: parallel_elapsed < 0.6s: True

    expected_log = ["A0", "B0", "A1", "B1", "A2", "B2"]  # => the exact interleave order to require
    assert interleaved_log == expected_log  # => confirms A and B alternate, never both "at once"
    assert parallel_elapsed < 0.6  # => confirms the two 0.3s CPU processes overlapped (not 0.6s serial)
    print("ex-01 OK")  # => Output: ex-01 OK
