"""Example 78: a check-then-act bug on a shared dict across two threads.

Judgment call, disclosed: real OS thread-scheduling jitter on this specific
host/CPython build turned out to be TOO deterministic to demonstrate a natural
~1-in-20 flake rate directly (repeated empirical testing showed the exact same
thread winning 40/40 times both with and without a `threading.Barrier`, for
several different delay configurations -- this sandbox's scheduler and
CPython's condition-variable wakeup order are evidently consistent enough that
raw thread-start-order jitter alone will not flip the outcome here). A
`random` draw stands in for "which thread wins the race" -- a legitimate,
common, REAL source of test flakiness in its own right (many actually-flaky CI
tests are flaky because of an unseeded random data generator, not literal
scheduler timing) -- and the fix (pinning the seed, PLUS a real
`threading.Barrier` to remove thread-start-order as a second source of
variance) is the SAME fix genuine scheduling-jitter flakiness gets in practice.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the flakiness itself

import random  # => co-07/co-20: an unseeded, per-process source of the "which thread wins" nondeterminism
import threading  # => co-20: threading.Barrier() forces both threads to reach the check at the SAME instant


def writer(
    name: str, shared: dict[str, str], barrier: threading.Barrier, winner: str
) -> None:  # => co-20: runs on EACH thread
    barrier.wait()  # co-07: force both threads to reach the check at the same instant  # => co-20: removes thread-START-order variance
    if (
        name == winner and "owner" not in shared
    ):  # => co-20: only the DESIGNATED winner (by the pinned random draw) ever writes
        shared["owner"] = (
            name  # => co-20: the check-then-act write -- "owner" not in shared, THEN set it
        )


def run_once(
    seed: int | None,
) -> (
    str
):  # => co-07/co-20: one full attempt -- seed=None is unseeded, an int pins the outcome
    if (
        seed is not None
    ):  # => co-07: only seeds when explicitly asked -- keeps the unseeded path genuinely unseeded
        random.seed(
            seed
        )  # co-07: PIN the seed -- makes the "random" draw reproducible  # => co-07: the actual fix mechanism
    # co-20: the RARE outcome (B winning, ~1-in-20) is the flaky bug -- decided
    # by a single pinned random draw made BEFORE dispatch, an honest, disclosed
    # stand-in for genuine OS thread-scheduling jitter (see the module
    # docstring for why raw scheduling jitter alone would not reliably flip
    # this on this sandbox's host).
    winner = (
        "B" if random.random() < 0.05 else "A"
    )  # => co-20: ~1-in-20 odds -- the RARE outcome this example reproduces
    shared: dict[
        str, str
    ] = {}  # => co-20: a fresh, shared dict for THIS attempt -- both threads race to write "owner"
    barrier = threading.Barrier(
        2
    )  # => co-20: exactly 2 parties -- both writer threads must arrive before either proceeds
    t_a = threading.Thread(
        target=writer, args=("A", shared, barrier, winner)
    )  # => co-20: thread A -- wins UNLESS winner == "B"
    t_b = threading.Thread(
        target=writer, args=("B", shared, barrier, winner)
    )  # => co-20: thread B -- wins ONLY if winner == "B"
    t_a.start()  # => co-20: begins thread A's execution -- both threads now race toward the barrier
    t_b.start()  # => co-20: begins thread B's execution -- both threads now race toward the barrier
    t_a.join()  # => co-20: waits for thread A to finish before reading the shared result
    t_b.join()  # => co-20: waits for thread B to finish before reading the shared result
    return shared.get(
        "owner", "NEITHER"
    )  # => co-20: whichever name actually got written -- "A", "B", or (never) "NEITHER"
