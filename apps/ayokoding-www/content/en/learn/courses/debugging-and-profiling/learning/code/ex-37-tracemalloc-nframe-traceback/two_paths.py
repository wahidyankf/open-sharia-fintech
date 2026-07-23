"""Example 37: tracemalloc's nframe Traceback -- two allocation PATHS that share one common frame."""

from __future__ import annotations

import tracemalloc

LEAKED: list[bytes] = []
TEMP: list[bytes] = []


def allocate(n: int) -> bytes:  # the ONE shared frame both paths funnel through
    return b"x" * n


def path_a_leaks() -> None:
    for _ in range(3000):
        LEAKED.append(allocate(1024))  # kept forever -- the REAL leak


def path_b_temporary() -> None:
    for _ in range(3000):
        TEMP.append(allocate(1024))
    TEMP.clear()  # released immediately after -- NOT a leak


def main() -> None:
    tracemalloc.start(1)  # nframe=1: only the immediate allocating frame is recorded
    path_a_leaks()
    path_b_temporary()
    snap_shallow = tracemalloc.take_snapshot()
    print("nframe=1 (shallow) -- both paths collapse onto the SAME 'allocate' frame:")
    for stat in snap_shallow.statistics("lineno")[:2]:
        print(" ", stat)

    tracemalloc.stop()
    tracemalloc.start(5)  # nframe=5: enough frames to distinguish the TWO call paths
    LEAKED.clear()
    TEMP.clear()
    path_a_leaks()
    path_b_temporary()
    snap_deep = tracemalloc.take_snapshot()
    print("\nnframe=5 (deep) -- traceback, grouped by full call PATH:")
    for stat in snap_deep.statistics("traceback")[:2]:
        print(" ", stat)
        for line in stat.traceback.format():
            print("   ", line)


if __name__ == "__main__":
    main()
