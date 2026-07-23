# learning/code/ex-45-p-class-sorting/p_class_sorting.py
"""Example 45: Poly-Time Sorting -- an O(n log n) Member of P."""  # => co-24: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import math  # => co-24: math.log2, for the theoretical n*log2(n) comparison curve
import random  # => co-24: generates the random input arrays this example times
import time  # => co-24: perf_counter -- measuring ACTUAL wall-clock scaling, not just asserting the theory


def measure_sort_time(n: int, seed: int = 0) -> float:  # => co-24: times Python's own Timsort on a random list
    """Time sorting a random list of n floats; returns elapsed seconds."""  # => co-24: documents measure_sort_time's contract -- no runtime output, just sets its __doc__
    rng = random.Random(seed)  # => co-24: a seeded RNG -- deterministic input across repeated runs
    data = [rng.random() for _ in range(n)]  # => co-24: n random floats, freshly generated for this size
    start = time.perf_counter()  # => co-24: begin timing window
    data.sort()  # => co-24: Python's builtin Timsort -- a POLY-TIME (O(n log n)) algorithm, the P-class member here
    return time.perf_counter() - start  # => co-24: elapsed wall-clock seconds for JUST the sort call


if __name__ == "__main__":  # => co-24: entry point -- this block runs only when the file executes directly, not on import
    sizes = [10_000, 20_000, 40_000, 80_000]  # => co-24: each size DOUBLES the previous one
    times = [measure_sort_time(n) for n in sizes]  # => co-24: one measured duration per size
    for n, t in zip(sizes, times):  # => co-24: prints size alongside its measured sort time
        theoretical = n * math.log2(n)  # => co-24: the O(n log n) shape this measurement is expected to track
        print(f"n={n:>7}  time={t:.4f}s  n*log2(n)={theoretical:,.0f}")  # => co-24: measured vs. theoretical shape
    ratios = [times[i + 1] / times[i] for i in range(len(times) - 1)]  # => co-24: measured time growth per doubling
    print(f"time ratios between successive doublings: {[round(r, 2) for r in ratios]}")  # => co-24: e.g. ~2.0-2.3x
    # A DOUBLING of n for an O(n log n) algorithm should grow the time by roughly the same small
    # multiple each time (2x plus a small log factor) -- nowhere NEAR the exponential blowup
    # Example 47's brute-force SAT solver will show. These are sub-10ms measurements, so exact
    # ratios jitter with system load; the assert below only checks the DIRECTION -- growth stays
    # well clear of exponential -- rather than pinning a tight numeric window (see Example 28 and
    # the capstone's memory.py for the same directional-only pattern on other timing measurements).
    assert all(r < 8 for r in ratios), "O(n log n) scaling must stay well under the exponential/factorial blowups Examples 47 and 49 measure"  # => co-24
    print(f"Sorting scales like O(n log n), not exponentially: True")  # => co-24: reached only if the assert passed
    # => co-24: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
