"""Example 57: the SAME race from ex-56, fixed with a threading.Lock -- rerun
the loop 100+ times and confirm every single run is exact.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fix itself

import threading  # => co-20/co-23: threading.Lock() is the ONE addition that fixes ex-56's race
import time  # => co-20: the SAME time.sleep(0) yield point -- still present, now safely inside the lock


def increment_many(
    counter_box: list[int], times: int, lock: threading.Lock
) -> None:  # => co-20/co-23: takes a shared lock now
    for _ in range(
        times
    ):  # => co-20: the SAME 200-iteration loop as ex-56's increment_many
        with lock:  # co-20/co-23: the read-sleep-write critical section is now atomic
            current = counter_box[
                0
            ]  # => co-23: the READ half -- now protected, no other thread can interleave
            time.sleep(
                0
            )  # =>  still yields the GIL, but the lock now protects this window
            counter_box[0] = (
                current + 1
            )  # => co-23: the WRITE half -- guaranteed to see ITS OWN read, unaltered


def run_once(
    n_threads: int, increments_per_thread: int
) -> int:  # => co-23: one full attempt, start to finish
    counter_box = [0]  # => co-23: the SAME shared, mutable counter as ex-56
    lock = (
        threading.Lock()
    )  # => co-20/co-23: ONE lock, shared by every thread below -- the actual fix
    threads = [  # => co-23: builds all 8 thread objects, each given the SAME lock instance
        threading.Thread(
            target=increment_many, args=(counter_box, increments_per_thread, lock)
        )  # => co-23: shares ONE lock
        for _ in range(n_threads)  # => co-23: 8 threads, exactly matching ex-56's shape
    ]  # => co-23: none started yet -- start() happens in the loop below
    for t in threads:  # => co-23: starts every thread -- they now race for the lock, not for the counter directly
        t.start()  # => co-23: begins real concurrent execution
    for t in (
        threads
    ):  # => co-23: waits for every thread to finish before reading the final count
        t.join()  # => co-23: blocks until this specific thread has completed
    return counter_box[
        0
    ]  # => co-23: the FINAL count -- should be exact on EVERY run now


def main() -> (
    None
):  # => co-23: reruns the race 100 times and confirms the lock makes every run exact
    n_threads = (
        8  # => co-23: the SAME 8 threads as ex-56, for a direct before/after comparison
    )
    increments_per_thread = 200  # => co-23: the SAME 200 increments per thread
    expected = (
        n_threads * increments_per_thread
    )  # => co-23: the mathematically correct final count, 1,600
    exact_count = (
        0  # => co-23: tallies how many of the 100 runs matched expected EXACTLY
    )
    for run_idx in range(
        100
    ):  # => co-23: the SAME 100-run sample size as ex-56, for a fair comparison
        result = run_once(
            n_threads, increments_per_thread
        )  # => co-23: one fresh counter_box, lock, and 8 threads
        if (
            result == expected
        ):  # => co-23: the lock should make this true on EVERY single run
            exact_count += 1  # => co-23: counts this run as exact
        else:  # => co-23: this branch should NEVER execute if the lock genuinely fixed the race
            print(
                f"run {run_idx}: got {result}, expected {expected} -- UNEXPECTED MISMATCH"
            )  # => co-23: would flag a real bug
    print(
        f"summary: {exact_count}/100 runs were EXACT (expected {expected} every time)"
    )  # => co-23: the headline result
    assert exact_count == 100, (
        f"expected all 100 runs exact, got {exact_count}/100"
    )  # => co-23: the real, strict check
    print(
        "confirmed: the lock makes every single run exact -- the race is fixed"
    )  # => co-23


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that runs all 100 attempts and reports the summary
