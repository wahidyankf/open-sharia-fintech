"""Example 48: run the SAME workload through cProfile at 100 items and 100,000 items."""

from __future__ import annotations

import cProfile
import pstats
import sys
from io import StringIO

sys.path.insert(0, ".")
from workload import make_items, process  # noqa: E402


def profile_at(n: int, repeat: int) -> str:
    # co-21: at n=100 a single pass finishes in microseconds -- too fast for
    # cProfile's per-call timer resolution to distinguish tottime meaningfully.
    # Repeating the SAME toy-scale call `repeat` times (a standard microbenchmark
    # trick) gives the profiler enough signal without changing which function is
    # actually the bottleneck at that scale.
    items = make_items(n)
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(repeat):
        process(items)
    profiler.disable()
    buf = StringIO()
    stats = pstats.Stats(profiler, stream=buf).sort_stats(pstats.SortKey.TIME)
    stats.print_stats(4)
    return buf.getvalue()


def main() -> None:
    # Judgment call: the syllabus's suggested realistic scale (1,000,000) makes
    # `dedupe_naive`'s TRUE O(n^2) blow-up (its "seen" list grows with n here,
    # since make_items' cardinality scales with n too) take on the order of
    # hours in pure Python. 100,000 already flips the bottleneck decisively
    # while finishing in a few seconds -- the property under test ("the
    # toy-scale hot spot differs from the realistic-scale one") is unaffected
    # by exactly which large n demonstrates it.
    print("=== toy scale: n=100 (x2000 repeats for timer resolution) ===")
    print(profile_at(100, repeat=2000))
    print("=== realistic scale: n=100_000 (single pass) ===")
    print(profile_at(100_000, repeat=1))


if __name__ == "__main__":
    main()
