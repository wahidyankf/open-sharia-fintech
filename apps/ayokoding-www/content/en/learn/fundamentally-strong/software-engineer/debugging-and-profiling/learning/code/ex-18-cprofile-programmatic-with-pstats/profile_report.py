"""Example 18: cProfile Programmatic API with pstats."""

from __future__ import annotations

import cProfile
import pstats
from pstats import SortKey

from report import (
    build_report,
    compute_total,
)  # reuses Example 17's scenario -- same functions


def main() -> None:
    data = [{"a": i * 1.5, "b": i * 2.5, "c": i * 0.5} for i in range(20_000)]
    profiler = cProfile.Profile()
    profiler.enable()
    build_report(data)
    compute_total(data)
    profiler.disable()

    stats = pstats.Stats(profiler)
    print("--- sorted by TIME (tottime, own time only) ---")
    stats.sort_stats(SortKey.TIME).print_stats(5)
    print("--- sorted by CUMULATIVE (cumtime, includes callees) ---")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats(5)


if __name__ == "__main__":
    main()
