"""Example 76: single caller vs many concurrent callers -- measure the gap
between WALL time and the sum of each call's own work time. Under a coarse
lock, concurrent callers spend real wall-clock time WAITING, not computing --
that gap only shows up under load, py-spy `top` would show this as threads
sitting in a "waiting" state (this substitute measures the same real effect
directly, since py-spy itself needs root on this host -- see ex-29/ex-71)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the measurement itself

import threading  # => co-21/co-15: real OS threads -- the SAME concurrency primitive whose contention this example measures
import time  # => co-21: time.perf_counter() -- measures REAL wall time, the thing the coarse lock inflates under load
import sys  # => needed only for sys.path.insert below

sys.path.insert(
    0, "."
)  # => makes local coarse_lock_handler.py importable regardless of caller's cwd
from coarse_lock_handler import handle_request  # noqa: E402  # => co-21: the coarse-locked function under measurement


def run_single(
    work_ms: float, n_calls: int
) -> float:  # => co-21: the NO-CONTENTION baseline -- one caller, no waiting
    start = time.perf_counter()  # => co-21: starts timing before any calls
    for _ in range(
        n_calls
    ):  # => co-21: n_calls sequential calls -- always 1 below, for a clean single-call baseline
        handle_request(
            work_ms
        )  # => co-21: no other thread contends for _coarse_lock here -- pure work time
    return (
        time.perf_counter() - start
    )  # => co-21: the REAL wall time for n_calls sequential, uncontended calls


def run_concurrent(
    work_ms: float, n_threads: int
) -> float:  # => co-21/co-15/co-20: n_threads all contend for ONE lock
    threads = [
        threading.Thread(target=handle_request, args=(work_ms,))
        for _ in range(n_threads)
    ]  # => co-21: n_threads objects
    start = time.perf_counter()  # => co-21: starts timing BEFORE any thread runs
    for t in (
        threads
    ):  # => co-21: starts every thread -- they now compete for the SAME _coarse_lock
        t.start()  # => co-21: begins execution -- most threads immediately block waiting for the lock
    for t in (
        threads
    ):  # => co-21: waits for every thread to finish before stopping the timer
        t.join()  # => co-21: blocks until this specific thread has completed
    return (
        time.perf_counter() - start
    )  # => co-21: the REAL wall time for n_threads CONCURRENT, CONTENDED calls


def main() -> (
    None
):  # => co-21/co-20/co-15: runs single vs concurrent, and confirms the wall-vs-CPU gap only shows under load
    work_ms = 20.0  # => co-21: each call's own "work" duration -- fixed, so it's directly comparable across both runs
    n_threads = (
        8  # => co-21: 8 concurrent callers, all contending for the SAME coarse lock
    )

    single_wall = run_single(
        work_ms, n_calls=1
    )  # => co-21: the BASELINE -- one call's own work time, with zero contention
    print(
        f"single call: {single_wall * 1000:.1f}ms wall time (no contention -- this IS the work time)"
    )  # => co-21

    concurrent_wall = run_concurrent(
        work_ms, n_threads
    )  # => co-21: 8 threads, all serialized by the SAME coarse lock
    print(
        f"{n_threads} concurrent callers, same coarse lock: {concurrent_wall * 1000:.1f}ms wall time"
    )  # => co-21

    ideal_if_parallel = single_wall  # => co-21: if truly parallel, wall time would stay ~= one call's time
    ideal_if_fully_serialized = (
        single_wall * n_threads
    )  # => co-21: if fully serialized, wall time scales linearly

    print(
        f"ideal if independent (no lock):     ~{ideal_if_parallel * 1000:.1f}ms"
    )  # => co-21: the BEST case, for reference
    print(
        f"ideal if fully serialized (1 lock): ~{ideal_if_fully_serialized * 1000:.1f}ms"
    )  # => co-21: the WORST case, for reference

    # co-21/co-20/co-15: under load, the coarse lock serializes everything --
    # the wall time should be close to fully-serialized, NOT close to a single call.
    assert concurrent_wall > ideal_if_parallel * (
        n_threads * 0.5
    ), (  # => co-21: the real, quantified check
        "expected the coarse lock to serialize concurrent callers -- wall time should scale with n_threads"  # => co-21: assert message
    )  # => co-21: closes the multi-line assert
    print(
        "confirmed: the wall-vs-CPU gap (real waiting time) only shows up under concurrent load"
    )  # => co-21: the headline result


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that measures single vs concurrent and reports the comparison
