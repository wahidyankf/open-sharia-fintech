"""Example 5: I/O-Bound Threads Actually Help."""

import threading  # => co-06 threads applied to I/O-bound work, unlike ex-03's CPU-bound case
import time  # => `time.sleep` stands in for any blocking I/O call (network, disk, a DB driver)

SLEEP_SECONDS = 0.2  # => each "request" pretends to block on I/O for this long


def fake_io_call() -> None:  # => simulates one blocking network/disk call
    time.sleep(SLEEP_SECONDS)  # => releases the GIL while blocked (co-05) -- OTHER threads can run


def run_serial(count: int) -> float:  # => baseline: `count` I/O calls, one after another
    start = time.perf_counter()  # => start is the wall-clock time before any call begins
    for _ in range(count):  # => runs each fake_io_call() to completion before starting the next
        fake_io_call()  # => blocks THIS thread for SLEEP_SECONDS, back to back
    return time.perf_counter() - start  # => total wall time is close to count * SLEEP_SECONDS


def run_threaded(count: int) -> float:  # => same `count` I/O calls, but each on its own thread
    start = time.perf_counter()  # => start is the wall-clock time before any thread launches
    threads = [threading.Thread(target=fake_io_call) for _ in range(count)]
    # => builds `count` Thread objects, each independently sleeping
    for t in threads:  # => launches every thread
        t.start()  # => start() -- while one thread sleeps, the GIL is free for the next (co-05)
    for t in threads:  # => waits for every thread to finish
        t.join()  # => join() blocks until that specific thread's sleep call returns
    return time.perf_counter() - start  # => total wall time is close to ONE SLEEP_SECONDS, not count*


if __name__ == "__main__":  # => module entry point
    calls = 4  # => how many "I/O calls" this demo makes, both ways
    serial_time = run_serial(calls)  # => serial_time: ~4 * 0.2s = ~0.8s, back to back
    threaded_time = run_threaded(calls)  # => threaded_time: ~0.2s, all four overlap
    print(f"serial={serial_time:.2f}s threaded={threaded_time:.2f}s")  # => Output: serial=~0.8s threaded=~0.2s

    # => Unlike ex-03's CPU-bound case, `time.sleep` releases the GIL for its whole duration,
    # => so all 4 threads' sleeps overlap almost perfectly -- I/O-bound work DOES parallelize
    # => on threads even though the GIL still serializes any actual Python bytecode (co-05).
    assert threaded_time < serial_time * 0.5  # => confirms real overlap: far less than 4x one sleep
    print("ex-05 OK")  # => Output: ex-05 OK
