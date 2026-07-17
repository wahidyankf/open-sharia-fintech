"""Example 56: Amdahl's Law -- the Theoretical CEILING on Parallel Speedup."""

import time  # => measures ACTUAL wall time to compare against the THEORETICAL prediction
from concurrent.futures import ProcessPoolExecutor  # => co-24: genuine parallel workers, for the empirical half

SERIAL_UNITS = 2  # => units of work that CANNOT be parallelized -- always run one after another
PARALLEL_UNITS = 8  # => units of work that CAN be split across multiple processes
UNIT_ITERATIONS = 3_000_000  # => how much CPU work ONE "unit" represents


def amdahl_speedup(serial_fraction: float, processors: int) -> float:  # => co-28: the closed-form prediction
    parallel_fraction = 1.0 - serial_fraction  # => parallel_fraction: the portion that DOES benefit from more cores
    return 1.0 / (serial_fraction + parallel_fraction / processors)  # => Amdahl's formula itself


def do_units(n: int) -> int:  # => a top-level function -- REQUIRED for ProcessPoolExecutor to pickle it
    total = 0  # => accumulator -- forces real CPU work, proportional to `n`
    for i in range(n):  # => a tight loop -- the "one unit of work" this function represents
        total += i  # => trivial arithmetic; only the TIME this consumes matters for this example
    return total  # => returned so the result can still be checked for correctness


if __name__ == "__main__":  # => module entry point
    serial_fraction = SERIAL_UNITS / (SERIAL_UNITS + PARALLEL_UNITS)  # => serial_fraction: co-28's "S", from the workload's own shape
    processors = 4  # => how many worker processes the empirical run actually uses

    predicted_speedup = amdahl_speedup(serial_fraction, processors)  # => predicted_speedup: the theoretical ceiling
    print(f"serial_fraction={serial_fraction:.2f} predicted_speedup={predicted_speedup:.2f}x")
    # => Output: serial_fraction=0.20 predicted_speedup=2.50x

    start_one = time.perf_counter()  # => start_one: wall time before the SINGLE-worker (baseline) run
    for _ in range(SERIAL_UNITS + PARALLEL_UNITS):  # => runs EVERY unit, serial and parallel, one after another
        do_units(UNIT_ITERATIONS)  # => simulates "1 processor": nothing can overlap, everything is sequential
    one_worker_time = time.perf_counter() - start_one  # => one_worker_time: the single-processor baseline

    start_n = time.perf_counter()  # => start_n: wall time before the multi-worker run
    for _ in range(SERIAL_UNITS):  # => the SERIAL portion always runs sequentially, no matter how many processors
        do_units(UNIT_ITERATIONS)  # => cannot be parallelized -- this IS the workload's serial fraction
    with ProcessPoolExecutor(max_workers=processors) as pool:  # => the PARALLEL portion, split across `processors`
        list(pool.map(do_units, [UNIT_ITERATIONS] * PARALLEL_UNITS))  # => genuinely overlaps across processes
    n_worker_time = time.perf_counter() - start_n  # => n_worker_time: serial part + (parallel part / processors, roughly)

    measured_speedup = one_worker_time / n_worker_time  # => measured_speedup: what ACTUALLY happened, empirically
    print(f"measured_speedup={measured_speedup:.2f}x")  # => Output: measured_speedup=~2.1x-2.5x (close to predicted)

    # => Amdahl's Law says the maximum possible speedup is capped by the SERIAL fraction of a workload,
    # => no matter how many processors you throw at the PARALLEL fraction: `1 / (S + (1-S)/N)`. Here,
    # => 20% of the work is inherently serial, so even with 4 processors the theoretical ceiling is only
    # => 2.5x, not 4x -- and the empirically MEASURED speedup lands close to that same ceiling (co-28),
    # => confirming the formula isn't just abstract math -- it predicts real, observable wall-clock time.
    assert measured_speedup > 1.5  # => confirms parallelizing DID help meaningfully
    assert measured_speedup < predicted_speedup * 1.3  # => confirms measured speedup stayed near the theoretical ceiling
    print("ex-56 OK")  # => Output: ex-56 OK
