"""Example 3: The GIL Serializes CPU-Bound Threads."""

import threading  # => co-06 threads, but this example is about their CPU-bound cost
import time  # => measures wall-clock time to reveal the GIL's serialization

ITERATIONS = 4_000_000  # => tuned so one call takes a small, measurable fraction of a second


def cpu_task(n: int) -> int:  # => pure arithmetic, no I/O -- exactly what the GIL cannot parallelize
    total = 0  # => total is 0 -- accumulator, forces the interpreter to do real bytecode work
    for i in range(n):  # => a tight Python loop -- every iteration executes under the GIL (co-03)
        total += i  # => each `total += i` is itself a non-atomic load/add/store (co-10)
    return total  # => returns the checksum -- the VALUE doesn't matter, only the TIME spent


def run_serial() -> float:  # => baseline: run cpu_task twice, one after another, on ONE thread
    start = time.perf_counter()  # => start is the wall-clock time before any work begins
    cpu_task(ITERATIONS)  # => first call: runs to completion before the second starts
    cpu_task(ITERATIONS)  # => second call: runs only after the first returns
    return time.perf_counter() - start  # => total wall time for BOTH calls, back to back


def run_threaded() -> float:  # => same total work, but split across TWO threads
    start = time.perf_counter()  # => start is the wall-clock time before either thread launches
    threads = [threading.Thread(target=cpu_task, args=(ITERATIONS,)) for _ in range(2)]
    # => builds two Thread objects, each targeting cpu_task with the SAME iteration count
    for t in threads:  # => launches both threads
        t.start()  # => start() schedules the thread -- but only ONE runs Python bytecode at a time
    for t in threads:  # => waits for both to finish
        t.join()  # => join() blocks until that specific thread's cpu_task() call returns
    return time.perf_counter() - start  # => total wall time for both threads combined


if __name__ == "__main__":  # => module entry point
    serial_time = run_serial()  # => serial_time: two cpu_task calls run one after another
    threaded_time = run_threaded()  # => threaded_time: the SAME two calls, split across 2 threads
    print(f"serial={serial_time:.3f}s threaded={threaded_time:.3f}s")  # => Output: serial=...s threaded=...s

    # => If threads gave real parallelism, threaded_time would be near HALF of serial_time.
    # => Instead, the GIL lets only one thread run Python bytecode at a time (co-03), so
    # => threaded_time stays close to serial_time -- at best a little faster from OS scheduling
    # => noise, never anywhere near a 2x speedup.
    ratio = threaded_time / serial_time  # => ratio near 1.0 means "no real speedup" from threading
    print(f"ratio={ratio:.2f}")  # => Output: ratio=~0.9-1.1 (never anywhere near 0.5)

    assert ratio > 0.8  # => confirms threading did NOT deliver anything close to a 2x speedup
    print("ex-03 OK")  # => Output: ex-03 OK
