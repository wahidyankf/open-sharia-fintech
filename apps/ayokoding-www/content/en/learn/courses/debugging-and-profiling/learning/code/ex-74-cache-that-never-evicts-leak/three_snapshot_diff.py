"""Example 74: three tracemalloc snapshots -- before, after a burst of unique
keys, and after a SECOND burst -- confirming near-zero NET growth on the second
burst once the cache is bounded (unlike ex-36's unbounded version, which grew
proportionally every time)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the leak-check itself

import sys  # => needed only for sys.path.insert below
import tracemalloc  # => co-17: the stdlib memory-snapshot tool this whole example is built on, same as ex-36

sys.path.insert(
    0, "."
)  # => makes local cache_fixed.py importable regardless of caller's cwd
from cache_fixed import BoundedCache  # noqa: E402  # => co-17: the FIXED cache under test, not ex-36's leaking one


def main() -> (
    None
):  # => co-17/co-23: takes 3 snapshots and confirms the second burst adds near-zero net memory
    cache = BoundedCache(
        max_size=500
    )  # => co-17: a small, fixed cap -- both bursts below vastly exceed it
    tracemalloc.start()  # => co-17: begins tracking every allocation from this point forward

    snapshot_0 = (
        tracemalloc.take_snapshot()
    )  # => co-17: the BASELINE, before any cache activity at all

    for i in range(
        5000
    ):  # => co-17: the FIRST burst -- 5,000 distinct keys, 10x the cache's own max_size
        cache.get_or_compute(
            f"key-{i}"
        )  # => co-17: every key is a genuine cache MISS -- all unique
    snapshot_1 = (
        tracemalloc.take_snapshot()
    )  # => co-17: captures memory state right after the first burst

    for i in range(
        5000, 10000
    ):  # => co-17: the SECOND burst -- 5,000 MORE distinct keys, same size as the first
        cache.get_or_compute(
            f"key-{i}"
        )  # => co-17: also all unique -- every insert should trigger an eviction now
    snapshot_2 = (
        tracemalloc.take_snapshot()
    )  # => co-17: captures memory state right after the second burst

    diff_0_to_1 = snapshot_1.compare_to(
        snapshot_0, "lineno"
    )  # => co-17: per-line memory delta across the FIRST burst
    diff_1_to_2 = snapshot_2.compare_to(
        snapshot_1, "lineno"
    )  # => co-17: per-line memory delta across the SECOND burst

    growth_0_to_1 = sum(
        stat.size_diff for stat in diff_0_to_1
    )  # => co-17: total bytes added during the first burst
    growth_1_to_2 = sum(
        stat.size_diff for stat in diff_1_to_2
    )  # => co-17: total bytes added during the second burst

    print(
        f"growth from snapshot 0 -> 1 (first 5,000 keys): {growth_0_to_1 / 1024:.1f} KiB"
    )  # => co-17: the first burst's cost
    print(
        f"growth from snapshot 1 -> 2 (next 5,000 keys):  {growth_1_to_2 / 1024:.1f} KiB"
    )  # => co-17: the payoff number
    print(
        f"cache size after both bursts: {len(cache._store)} entries (bounded at max_size=500)"
    )  # => co-17: confirms the cap held

    # co-17/co-23: the second burst should NOT keep growing memory proportionally
    # -- the cache is bounded, so old entries get evicted as new ones arrive.
    assert len(cache._store) == 500, (
        f"expected the cache to stay bounded at 500, got {len(cache._store)}"
    )  # => co-17: the real check
    assert (
        growth_1_to_2 < growth_0_to_1 / 3
    ), (  # => co-17/co-23: the SECOND burst's growth must be MUCH smaller than the first's
        f"expected near-zero net growth on the second burst ({growth_1_to_2} bytes) "  # => co-17: message part 1
        f"compared to the first ({growth_0_to_1} bytes)"  # => co-17: message part 2, closes the assert's message
    )  # => co-17: closes the multi-line assert
    print(
        "confirmed: the third snapshot shows near-zero net growth -- the eviction fix works"
    )  # => co-17: the headline result


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that takes all three snapshots and reports the comparison
