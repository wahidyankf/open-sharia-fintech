"""Example 56: a plain-int increment race across threads -- no lock, 100 runs.

Judgment call, disclosed: a bare `counter_box[0] += 1` tight loop turned out NOT
to reproduce lost updates on this host/CPython build even across millions of
iterations -- CPython 3.13's specializing adaptive interpreter checks the
eval-breaker (the point where the GIL can be handed to another thread) far less
often than older CPython versions did, so a single-bytecode-window critical
section rarely gets interrupted mid-read-modify-write here. Real-world races
almost never look like a single bytecode instruction anyway -- there is real
work between the read and the write (a computed value, a second field update, an
I/O wait). This example widens that window with one explicit `time.sleep(0)`
between the read and the write -- a real, honest stand-in for "there is
non-trivial work in the critical section", not a fabricated result.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the race itself

import threading  # => co-20: the concurrency primitive whose lack of synchronization causes the race
import time  # => co-20: time.sleep(0) is what widens the read-modify-write window enough to lose updates


def increment_many(
    counter_box: list[int], times: int
) -> None:  # => co-20: runs on EACH of the 8 threads below
    for _ in range(
        times
    ):  # => co-20: 200 increments per thread -- 1,600 total across 8 threads
        # co-20: read-modify-write with NO lock, and a real yield point
        # (time.sleep(0)) between the read and the write -- representing the
        # "some real work happens here" gap that makes races reproducible in
        # practice, not just in theory.
        current = counter_box[
            0
        ]  # => co-20: the READ half -- another thread can run before the WRITE below
        time.sleep(0)  # => hands the GIL to another thread, widening the window
        counter_box[0] = (
            current + 1
        )  # => co-20: the WRITE half -- may overwrite another thread's own increment


def run_once(
    n_threads: int, increments_per_thread: int
) -> int:  # => co-20: one full race attempt, start to finish
    counter_box = [
        0
    ]  # => co-20: a one-element list -- mutable, so every thread shares the SAME counter object
    threads = [  # => co-20: builds all 8 thread objects up front, none started yet
        threading.Thread(
            target=increment_many, args=(counter_box, increments_per_thread)
        )
        for _ in range(n_threads)
    ]  # => co-20: each thread races to read-sleep-write the SAME counter_box
    for t in (
        threads
    ):  # => co-20: starts every thread -- they now run concurrently, racing each other
        t.start()  # => co-20: begins execution on a real OS thread, GIL-scheduled
    for t in (
        threads
    ):  # => co-20: waits for every thread to finish before reading the final count
        t.join()  # => co-20: blocks until this specific thread has completed
    return counter_box[
        0
    ]  # => co-20: the FINAL count -- may be below the expected 1,600 if updates were lost


def main() -> (
    None
):  # => co-20: runs the race 100 times and reports how often it actually loses updates
    n_threads = (
        8  # => co-20: 8 concurrent threads, all incrementing the same shared counter
    )
    increments_per_thread = (
        200  # => co-20: 200 increments each -- 1,600 total if NOTHING is ever lost
    )
    expected = (
        n_threads * increments_per_thread
    )  # => co-20: the mathematically correct final count
    below_expected_count = (
        0  # => co-20: tallies how many of the 100 runs actually showed lost updates
    )
    lost_totals: list[
        int
    ] = []  # => co-20: records HOW MANY increments were lost, per failing run
    for run_idx in range(
        100
    ):  # => co-20: 100 independent attempts -- races are probabilistic, not guaranteed
        result = run_once(
            n_threads, increments_per_thread
        )  # => co-20: one fresh counter_box and 8 fresh threads
        if (
            result != expected
        ):  # => co-20: any deviation from 1,600 means at least one increment was lost
            below_expected_count += (
                1  # => co-20: counts this run as a demonstrated race
            )
            lost_totals.append(
                expected - result
            )  # => co-20: records the size of the loss for this run
    print(
        f"summary: {below_expected_count}/100 runs showed a final count below expected {expected}"
    )  # => co-20
    if (
        lost_totals
    ):  # => co-20: only prints examples if at least one run actually lost updates
        print(
            f"example lost-increment counts from a few of those runs: {lost_totals[:5]}"
        )  # => co-20: a small sample
    assert below_expected_count >= 1, (
        "expected at least one run to demonstrate the race"
    )  # => co-20: the real check
    print(
        "confirmed: the unsynchronized counter lost real increments under real concurrent access"
    )  # => co-20


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that runs all 100 attempts and reports the summary
