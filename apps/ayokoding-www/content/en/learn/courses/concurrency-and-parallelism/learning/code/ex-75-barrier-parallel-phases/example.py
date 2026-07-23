"""Example 75: A `Barrier` Synchronizes Phased Parallel Computation."""

import threading  # => co-15, co-28: a Barrier enforces "everyone finishes phase N before ANYONE starts N+1"
import time  # => `time.sleep` gives each worker a DIFFERENT phase-1 duration, to genuinely test the rendezvous

WORKER_COUNT = 4  # => four independent workers, each moving through the SAME three phases


def phased_worker(worker_id: int, barrier: threading.Barrier, phase1_end: list[float], phase2_start: list[float]) -> None:
    # => moves through phase 1, a rendezvous, phase 2, and a second rendezvous -- twice per worker
    time.sleep(0.01 * worker_id)  # => DIFFERENT workers take DIFFERENT amounts of time for phase 1
    phase1_end[worker_id] = time.perf_counter()  # => records exactly when THIS worker's phase 1 finished
    barrier.wait()  # => BLOCKS here until ALL WORKER_COUNT workers have reached this SAME point
    phase2_start[worker_id] = time.perf_counter()  # => records exactly when THIS worker's phase 2 began
    barrier.wait()  # => a SECOND rendezvous -- phase 2 is also fully complete before ANY worker moves on


def run_phased_computation() -> tuple[list[float], list[float]]:
    barrier = threading.Barrier(WORKER_COUNT)  # => barrier: releases ONLY once all WORKER_COUNT threads arrive
    phase1_end: list[float] = [0.0] * WORKER_COUNT  # => phase1_end[i]: when worker i finished phase 1
    phase2_start: list[float] = [0.0] * WORKER_COUNT  # => phase2_start[i]: when worker i began phase 2
    workers = [
        # => all workers share the SAME barrier -- that shared object IS the synchronization point
        threading.Thread(target=phased_worker, args=(i, barrier, phase1_end, phase2_start))
        for i in range(WORKER_COUNT)  # => one thread per worker, each with its OWN staggered phase-1 delay
    ]  # => workers: exactly WORKER_COUNT Thread objects, not yet started
    for w in workers:  # => starts every worker
        w.start()  # => each begins its own (different-length) phase 1 immediately
    for w in workers:  # => waits for every worker to finish BOTH phases
        w.join()  # => join() blocks until that worker's phased_worker() call returns
    return phase1_end, phase2_start  # => everything needed to verify the phase-ordering invariant


if __name__ == "__main__":  # => module entry point
    phase1_end, phase2_start = run_phased_computation()  # => drives the whole three-phase scenario to completion
    print(f"phase1_end={[round(t, 3) for t in phase1_end]}")  # => Output: phase1_end=[<staggered times>]
    print(f"phase2_start={[round(t, 3) for t in phase2_start]}")  # => Output: phase2_start=[<roughly IDENTICAL times>]

    latest_phase1_end = max(phase1_end)  # => latest_phase1_end: the SLOWEST worker's phase-1 finish time
    earliest_phase2_start = min(phase2_start)  # => earliest_phase2_start: the FASTEST worker's phase-2 start time

    # => Without the Barrier, faster workers (worker 0's near-instant phase 1) would race ahead into
    # => phase 2 long before the slowest worker (worker 3's 0.03s-delayed phase 1) finishes ITS phase 1
    # => -- exactly the kind of bug phased parallel algorithms (co-28) can't tolerate. `barrier.wait()`
    # => guarantees NO worker's phase 2 can start until EVERY worker has finished phase 1 (co-15): the
    # => earliest possible phase-2 start is bounded below by the LATEST phase-1 finish, across ALL workers.
    assert earliest_phase2_start >= latest_phase1_end  # => confirms the phase boundary was genuinely enforced
    print("ex-75 OK")  # => Output: ex-75 OK
