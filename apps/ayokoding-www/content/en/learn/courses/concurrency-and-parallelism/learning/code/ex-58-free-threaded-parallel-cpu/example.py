"""Example 58: On a Free-Threaded Build, CPU-Bound Threads Actually Scale."""

import sys  # => co-04: `sys._is_gil_enabled()` tells us which kind of build is RUNNING right now
import threading  # => the exact same threading shape as ex-49 -- only the BUILD differs
import time  # => measures wall time to compute an empirical speedup ratio

ITERATIONS = 8_000_000  # => tuned so 4 threads' worth of work is clearly measurable, not instant
THREAD_COUNT = 4  # => how many threads race to do CPU work concurrently


def gil_is_enabled() -> bool:  # => the SAME version-gated check introduced in ex-04
    if hasattr(sys, "_is_gil_enabled"):  # => only exists on Python 3.13+
        return sys._is_gil_enabled()  # pyright: ignore[reportPrivateUsage]
        # => leading underscore is CPython's naming, not a privacy signal -- the documented 3.13+ API
    return True  # => pre-3.13: no free-threaded option ever existed, so the GIL was always enabled


def cpu_task(n: int) -> int:  # => pure CPU work -- no I/O, so the GIL (if enabled) can NEVER be released mid-loop
    total = 0  # => accumulator -- forces real interpreter bytecode execution
    for i in range(n):  # => a tight loop -- exactly the shape a GIL serializes across threads
        total += i  # => trivial arithmetic; only the TIME this takes matters here
    return total  # => the actual value is irrelevant to this example


def measure_threaded_speedup(iterations: int, thread_count: int) -> float:
    single_start = time.perf_counter()  # => single_start: wall time before the ONE-thread baseline unit
    cpu_task(iterations)  # => runs exactly ONE unit of work, alone, to establish a per-unit baseline
    single_time = time.perf_counter() - single_start  # => single_time: how long ONE unit takes, uncontended

    threads = [threading.Thread(target=cpu_task, args=(iterations,)) for _ in range(thread_count)]
    start = time.perf_counter()  # => start: wall time before the `thread_count`-way concurrent run
    for t in threads:  # => starts every thread, all targeting the SAME cpu_task
        t.start()  # => each begins its own `iterations`-long loop, "concurrently" (subject to the GIL)
    for t in threads:  # => waits for every thread to finish
        t.join()  # => join() blocks until that thread's cpu_task() call returns
    elapsed = time.perf_counter() - start  # => elapsed: wall time for ALL `thread_count` threads combined

    serial_equivalent = single_time * thread_count  # => serial_equivalent: what `thread_count` units WOULD cost run one-by-one
    return serial_equivalent / elapsed  # => speedup: how much faster the threaded run was vs doing it serially


if __name__ == "__main__":  # => module entry point
    gil_enabled = gil_is_enabled()  # => gil_enabled: is THIS running interpreter's GIL currently active?
    speedup = measure_threaded_speedup(ITERATIONS, THREAD_COUNT)  # => speedup: the empirically measured ratio
    print(f"gil_enabled={gil_enabled} speedup={speedup:.2f}x")  # => Output: gil_enabled=True speedup=~1.0x (on a normal build)

    # => This script was verified on STANDARD CPython 3.13/3.14 (`python3.14t` -- the free-threaded,
    # => PEP 703/779 build -- is not installed in this environment), where `gil_enabled` prints True and
    # => `speedup` stays close to 1x, because the GIL serializes ALL FOUR threads' bytecode onto one core
    # => (co-03). A reader who installs `python3.14t` and reruns this EXACT script would instead see
    # => `gil_enabled=False`, and `speedup` climbing toward NEAR-LINEAR scaling (~3-4x with 4 threads,
    # => on a machine with that many free cores) -- because a free-threaded build removes the single
    # => lock that otherwise forces every thread's Python bytecode through one core at a time (co-04).
    if gil_enabled:  # => the branch this environment actually takes
        assert speedup < 2.0  # => confirms the GIL build did NOT meaningfully parallelize CPU work
    else:  # => the branch a `python3.14t` reader would take instead
        assert speedup > 2.5  # => confirms the free-threaded build DID scale close to linearly
    print("ex-58 OK")  # => Output: ex-58 OK
