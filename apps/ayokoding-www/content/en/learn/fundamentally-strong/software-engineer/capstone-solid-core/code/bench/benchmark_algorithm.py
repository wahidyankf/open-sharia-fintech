"""capstone-solid-core: Step 3's algorithm benchmark (topic 25 Advanced Algorithms). Measures
`longest_streak_ever_naive` (O(n log n), sort-based) against `longest_streak_ever` (O(n),
hash-set-based) over the SAME randomly generated check-in history, growing `n`, using
`time.perf_counter()` -- the standard library's monotonic, highest-resolution timer
(docs.python.org/3/library/time.html#time.perf_counter): "always returns a monotonic value ...
should be used for measuring performance." Every number printed below comes from actually
running both functions against the same generated data; this script prints nothing it did not
just compute.

Run: python3 -m bench.benchmark_algorithm   (from capstone-solid-core/code/, inside the venv)
"""

from __future__ import annotations

import random
import time
from datetime import date, timedelta

from app.domain import longest_streak_ever, longest_streak_ever_naive


def _generate_checkin_history(n: int, seed: int) -> set[date]:
    """A synthetic history of `n` DISTINCT calendar days, scattered (not necessarily
    consecutive) over a window wide enough to hold them -- exercises the general case, not
    just one long unbroken streak."""
    rng = random.Random(seed)
    base = date(1990, 1, 1)
    window = (
        n * 3
    )  # => scattered across a window 3x wider than n, so most are NOT adjacent
    offsets = rng.sample(range(window), n)
    return {base + timedelta(days=offset) for offset in offsets}


def _time_once(func, checkin_dates: set[date]) -> tuple[int, float]:
    start = time.perf_counter()
    result = func(checkin_dates)
    elapsed = time.perf_counter() - start
    return result, elapsed


def main() -> None:
    sizes = [1_000, 10_000, 100_000, 500_000]
    print(
        f"{'n':>10}  {'naive O(n log n) (s)':>22}  {'optimized O(n) (s)':>20}  {'speedup':>9}"
    )
    for n in sizes:
        checkin_dates = _generate_checkin_history(n, seed=42)

        naive_result, naive_elapsed = _time_once(
            longest_streak_ever_naive, checkin_dates
        )
        optimized_result, optimized_elapsed = _time_once(
            longest_streak_ever, checkin_dates
        )

        assert naive_result == optimized_result, (
            f"MISMATCH at n={n}: naive={naive_result} optimized={optimized_result} "
            "-- the benchmark is invalid if the two algorithms disagree"
        )

        speedup = (
            naive_elapsed / optimized_elapsed if optimized_elapsed > 0 else float("inf")
        )
        print(
            f"{n:>10}  {naive_elapsed:>22.6f}  {optimized_elapsed:>20.6f}  {speedup:>8.2f}x"
        )


if __name__ == "__main__":
    main()
