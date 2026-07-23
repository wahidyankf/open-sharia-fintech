"""Example 60: a genuinely CPU-bound job (no I/O), run 4 ways in parallel via
threading vs multiprocessing -- the GIL means threading's wall time stays close
to ONE worker's own CPU time, while multiprocessing's wall time drops toward
total-CPU-time / core-count.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the comparison itself

import multiprocessing  # => co-15: real, separate OS processes -- each gets its OWN GIL, genuine parallelism
import os  # => co-15: os.cpu_count() -- reports how many cores multiprocessing could theoretically use
import threading  # => co-14: real OS threads -- but ALL share ONE GIL for this CPU-bound job
import time  # => co-14/co-15: time.perf_counter() -- measures WALL time, the thing that actually differs here


def cpu_bound_work(
    n: int,
) -> (
    int
):  # => co-14/co-15: pure Python bytecode loop -- no I/O, no C-level release of the GIL
    total = 0  # => the accumulator -- its final value is irrelevant, only the WORK matters here
    for i in range(
        n
    ):  # => co-14/co-15: n iterations of pure interpreter work -- the thing GIL contention affects
        total += (
            i * i
        )  # => co-14/co-15: cheap per-iteration math -- keeps this CPU-bound, not memory-bound
    return (
        total  # => discarded by every caller below -- only the ELAPSED TIME is measured
    )


def run_threaded(
    n_workers: int, n_per_worker: int
) -> float:  # => co-14: n_workers OS threads, ONE shared GIL
    threads = [
        threading.Thread(target=cpu_bound_work, args=(n_per_worker,))
        for _ in range(n_workers)
    ]  # => co-14
    start = (
        time.perf_counter()
    )  # => co-14: starts the wall-clock timer BEFORE any thread runs
    for (
        t
    ) in threads:  # => co-14: starts every thread -- they now compete for the SAME GIL
        t.start()  # => co-14: begins execution, GIL-scheduled between all n_workers threads
    for t in (
        threads
    ):  # => co-14: waits for every thread to finish before stopping the timer
        t.join()  # => co-14: blocks until this specific thread has completed
    return (
        time.perf_counter() - start
    )  # => co-14: the WALL time all n_workers threads together took


def run_multiprocess(
    n_workers: int, n_per_worker: int
) -> float:  # => co-15: n_workers SEPARATE processes, SEPARATE GILs
    procs = [
        multiprocessing.Process(target=cpu_bound_work, args=(n_per_worker,))
        for _ in range(n_workers)
    ]  # => co-15
    start = (
        time.perf_counter()
    )  # => co-15: starts the wall-clock timer BEFORE any process runs
    for p in procs:  # => co-15: starts every process -- each runs on its OWN core, no GIL contention between them
        p.start()  # => co-15: forks/spawns a real OS process
    for (
        p
    ) in procs:  # => co-15: waits for every process to finish before stopping the timer
        p.join()  # => co-15: blocks until this specific process has completed
    return (
        time.perf_counter() - start
    )  # => co-15: the WALL time all n_workers processes together took


def main() -> (
    None
):  # => co-14/co-15/co-21: runs single-worker, threaded, and multiprocess, then compares
    n_workers = 4  # => co-14/co-15: the SAME worker count for BOTH threading and multiprocessing runs
    n_per_worker = 15_000_000  # => co-14/co-15: large enough that startup overhead is negligible next to the work
    n_cores = (
        os.cpu_count() or 1
    )  # => co-21: reports the host's real core count, for context in the printed summary
    print(
        f"host reports {n_cores} CPU cores; running {n_workers} workers"
    )  # => co-21: names the hardware this run used

    single_start = (
        time.perf_counter()
    )  # => co-14/co-15: the BASELINE -- one worker's own CPU-bound cost, alone
    cpu_bound_work(
        n_per_worker
    )  # => co-14/co-15: runs the SAME work size as each individual thread/process below
    single_wall = (
        time.perf_counter() - single_start
    )  # => co-14/co-15: the per-worker CPU-time baseline both ratios use
    print(
        f"ONE worker alone: {single_wall:.3f}s wall time (this is our per-worker CPU-time baseline)"
    )  # => co-14/co-15

    threaded_wall = run_threaded(
        n_workers, n_per_worker
    )  # => co-14: expect close to single_wall * n_workers (GIL-serialized)
    print(
        f"{n_workers} threads (co-14: GIL-serialized):        {threaded_wall:.3f}s wall time"
    )  # => co-14

    mp_wall = run_multiprocess(
        n_workers, n_per_worker
    )  # => co-15: expect well under single_wall * n_workers (real cores)
    print(
        f"{n_workers} processes (co-15: real parallel cores): {mp_wall:.3f}s wall time"
    )  # => co-15

    threaded_ratio = (
        threaded_wall / single_wall
    )  # => co-14: how many multiples of the baseline threading actually cost
    mp_ratio = (
        mp_wall / single_wall
    )  # => co-15: the SAME ratio, computed the SAME way, for direct comparison
    print(
        f"threaded wall / single-worker wall: {threaded_ratio:.2f}x  (expect close to {n_workers}x -- GIL serializes)"
    )  # => co-14
    print(
        f"mp wall / single-worker wall:       {mp_ratio:.2f}x  (expect well under {n_workers}x -- real parallelism)"
    )  # => co-15

    assert (
        threaded_ratio > mp_ratio
    ), (  # => co-14/co-15/co-21: the real, quantified claim this example proves
        f"expected threading ({threaded_ratio:.2f}x) to scale worse than multiprocessing ({mp_ratio:.2f}x) "  # => co-21: message part 1
        "for this CPU-bound job"  # => co-21: message part 2 -- concatenated with the line above
    )  # => co-21: closes the assert's multi-line message
    print(
        "confirmed: threading's wall time tracks near-serial CPU-bound cost; multiprocessing's wall time drops"
    )  # => co-14/co-15


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that runs all three measurements and reports the comparison
