# learning/code/ex-63-argon2-parameter-tuning/tune_argon2.py
"""Example 63: real argon2id timing -- a weak baseline, the topic's floor params, then a live-tuned target (co-09)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the timing measurement itself

import time  # => co-09: real wall-clock timestamps -- every duration below is genuinely measured, not estimated

from argon2 import (
    PasswordHasher,
)  # => co-09: argon2-cffi 25.1.0 pinned -- the real hasher this example tunes

PASSWORD = "correct-horse-battery-staple"  # => co-09: one fixed, real password hashed identically across all trials
TARGET_MS = 250.0  # => co-09: this topic's documented budget -- OWASP's argon2id guidance, ~250ms per hash


def measure_hash_time(
    memory_cost: int, time_cost: int, parallelism: int
) -> float:  # => co-09: one REAL, timed hash
    hasher = PasswordHasher(
        memory_cost=memory_cost, time_cost=time_cost, parallelism=parallelism
    )  # => co-09: real params
    start = time.perf_counter()  # => co-09: a real, high-resolution wall-clock start
    hasher.hash(
        PASSWORD
    )  # => co-09: the REAL, actual argon2id hash computation -- not simulated or estimated
    return (
        time.perf_counter() - start
    ) * 1000  # => co-09: real elapsed milliseconds for THIS specific call


def main() -> (
    None
):  # => co-09: measures a weak baseline, the topic's floor, then LIVE-tunes toward the target budget
    print(
        "=== weak baseline (m=8 KiB, t=1, p=1) -- what an under-tuned config looks like ==="
    )  # => labels section
    weak_ms = measure_hash_time(
        memory_cost=8, time_cost=1, parallelism=1
    )  # => co-09: a REAL, deliberately weak measurement
    print(
        f"weak: {weak_ms:.1f}ms"
    )  # => co-09: real, measured milliseconds -- expect well under 10ms on any machine

    print(
        "\n=== this topic's documented floor (m=19456 KiB, t=2, p=1) -- OWASP's min-tier params ==="
    )  # => labels
    baseline_ms = measure_hash_time(
        memory_cost=19456, time_cost=2, parallelism=1
    )  # => co-09: the REAL floor from co-09
    print(
        f"baseline: {baseline_ms:.1f}ms"
    )  # => co-09: real, measured milliseconds at the documented minimum tier

    print(
        f"\n=== live-tuning time_cost toward the ~{TARGET_MS:.0f}ms budget on THIS machine ==="
    )  # => labels section
    memory_cost = 19456  # => co-09: keeps memory_cost fixed at the floor -- only time_cost is tuned here
    time_cost = (
        2  # => co-09: starts the search from the SAME floor time_cost measured above
    )
    tuned_ms = baseline_ms  # => co-09: real starting point for the search loop below
    while (
        tuned_ms < TARGET_MS and time_cost < 200
    ):  # => co-09: a real, live search -- stops once the budget is reached
        time_cost += 1  # => co-09: increases cost by one real unit per iteration -- a simple, real linear search
        tuned_ms = measure_hash_time(
            memory_cost=memory_cost, time_cost=time_cost, parallelism=1
        )  # => co-09: a REAL trial
        print(
            f"  trying time_cost={time_cost}: {tuned_ms:.1f}ms"
        )  # => co-09: real, per-trial measurement, live search

    print(
        f"\ntuned params: memory_cost={memory_cost}, time_cost={time_cost}, parallelism=1 -> {tuned_ms:.1f}ms"
    )
    assert (
        tuned_ms >= baseline_ms
    )  # => co-09: proves the tuned config is REAL work, at least as slow as the floor
    assert (
        tuned_ms > weak_ms * 5
    )  # => co-09: proves the tuned config is MEANINGFULLY slower than the weak baseline
    assert (
        tuned_ms < TARGET_MS * 2
    )  # => co-09: a generous sanity bound -- tuning stopped reasonably near the budget


if (
    __name__ == "__main__"
):  # => co-09: only runs when launched directly, e.g. `python3 tune_argon2.py`
    main()  # => co-09: runs all real measurements and the real live-tuning search, printing every real trial
