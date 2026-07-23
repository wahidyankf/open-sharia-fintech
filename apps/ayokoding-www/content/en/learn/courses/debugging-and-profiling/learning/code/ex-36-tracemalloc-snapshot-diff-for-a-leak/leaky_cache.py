"""Example 36: A tracemalloc Snapshot Diff for a Leak."""

from __future__ import annotations

import tracemalloc

_CACHE: dict[str, bytes] = {}


def cache_response(key: str, payload: bytes) -> None:
    _CACHE[key] = (
        payload  # seeded bug: never evicted -- grows without bound as key keeps changing
    )


def simulate_requests(start: int, count: int) -> None:
    for i in range(start, start + count):
        cache_response(f"request-{i}", b"x" * 2048)


def main() -> None:
    tracemalloc.start()
    simulate_requests(0, 2000)
    snap_a = tracemalloc.take_snapshot()
    simulate_requests(2000, 2000)
    snap_b = tracemalloc.take_snapshot()
    diff = snap_b.compare_to(snap_a, "lineno")
    print("top 3 growth lines, N=2000 more requests:")
    for stat in diff[:3]:
        print(stat)

    simulate_requests(4000, 2000)
    snap_c = tracemalloc.take_snapshot()
    diff2 = snap_c.compare_to(snap_b, "lineno")
    print("\ntop 3 growth lines, ANOTHER 2000 requests (N doubled again):")
    for stat in diff2[:3]:
        print(stat)


if __name__ == "__main__":
    main()
