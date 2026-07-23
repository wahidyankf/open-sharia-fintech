"""Example 49: profile ONE call to handle_request, then run 8 threads calling it
concurrently, and show that lock-wait time is only visible under load.

A real, empirically confirmed limitation surfaces here: cProfile.Profile.enable()
is process-globally exclusive in CPython -- even two SEPARATE Profile() instances
enabled from two different threads at the same moment raise
"ValueError: Another profiling tool is already active" (reproduced below). So
cProfile itself cannot be the tool that measures concurrent contention; instead we
wrap the lock with real time.perf_counter() timestamps around every acquire(),
which is unaffected by cProfile's single-profiler-at-a-time restriction.
"""

from __future__ import annotations

import cProfile
import threading
import time

import handler


def demonstrate_cprofile_concurrency_limitation() -> str:
    # co-21: two separate Profile() instances, enabled concurrently from two
    # threads -- this is the real, reproducible error, captured once here so the
    # limitation is documented rather than asserted.
    profiler_a = cProfile.Profile()
    profiler_b = cProfile.Profile()
    errors: list[str] = []

    def enable_and_hold(profiler: cProfile.Profile) -> None:
        try:
            profiler.enable()
            time.sleep(0.05)
            profiler.disable()
        except ValueError as exc:
            errors.append(repr(exc))

    t_a = threading.Thread(target=enable_and_hold, args=(profiler_a,))
    t_b = threading.Thread(target=enable_and_hold, args=(profiler_b,))
    t_a.start()
    t_b.start()
    t_a.join()
    t_b.join()
    return "; ".join(errors) if errors else "(no error -- unexpected)"


class TimedLock:
    """A drop-in wrapper around threading.Lock that records real acquire-wait time.

    co-21: this is the honest workaround for cProfile's single-profiler
    exclusivity -- direct wall-clock instrumentation around the exact call that
    matters (Lock.acquire), which works correctly under real concurrency.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._wait_times: list[float] = []
        self._wait_times_guard = threading.Lock()  # =>  protects _wait_times itself

    def __enter__(self) -> "TimedLock":
        start = time.perf_counter()
        self._lock.acquire()
        elapsed = time.perf_counter() - start
        with self._wait_times_guard:
            self._wait_times.append(elapsed)
        return self

    def __exit__(self, *exc_info: object) -> None:
        self._lock.release()

    def total_wait(self) -> float:
        with self._wait_times_guard:
            return sum(self._wait_times)


def run_single_call() -> float:
    timed_lock = TimedLock()
    handler.handle_request_with_lock(1000, timed_lock)
    return timed_lock.total_wait()


def run_threaded_load(n_threads: int) -> float:
    timed_lock = TimedLock()
    threads = [
        threading.Thread(
            target=handler.handle_request_with_lock, args=(1000, timed_lock)
        )
        for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return timed_lock.total_wait()


def main() -> None:
    print("=== cProfile concurrency limitation (real, reproduced) ===")
    print(demonstrate_cprofile_concurrency_limitation())
    print()

    print(
        "=== single call, no contention (real wall-clock lock-wait instrumentation) ==="
    )
    single_wait = run_single_call()
    print(f"total time spent waiting inside Lock.acquire: {single_wait:.6f}s")
    print()

    print("=== 8 threads, real lock contention ===")
    threaded_wait = run_threaded_load(n_threads=8)
    print(f"total time spent waiting inside Lock.acquire: {threaded_wait:.6f}s")
    print()

    assert threaded_wait > single_wait * 5, (
        f"expected threaded lock-wait ({threaded_wait:.6f}s) to dwarf the single-call "
        f"baseline ({single_wait:.6f}s) -- contention should only show up under load"
    )
    print(
        f"confirmed: total lock-wait time is {threaded_wait / max(single_wait, 1e-9):.1f}x higher "
        "under 8-thread contention than in the uncontended single call"
    )


if __name__ == "__main__":
    main()
