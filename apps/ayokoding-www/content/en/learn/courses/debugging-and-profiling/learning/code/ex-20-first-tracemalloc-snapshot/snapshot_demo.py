"""Example 20: First tracemalloc Snapshot."""

from __future__ import annotations

import tracemalloc


def build_big_list(n: int) -> list[int]:
    return [
        i * i for i in range(n)
    ]  # the allocation this snapshot should point straight at


def main() -> None:
    tracemalloc.start()  # co-17: begins recording every Python allocation's traceback
    big = build_big_list(500_000)
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    print(f"len(big)={len(big)}")
    for stat in top_stats[:5]:
        print(stat)


if __name__ == "__main__":
    main()
