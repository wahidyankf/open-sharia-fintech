# learning/code/ex-27-latency-hierarchy-table/latency_hierarchy.py
"""Example 27: Approximate Register/Cache/RAM/Disk Latency Ratios."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from typing import NamedTuple  # => co-16: a typed record for each hierarchy level's approximate latency


class LatencyLevel(NamedTuple):  # => co-16: one rung of the memory hierarchy this example surveys
    name: str  # => co-16: the level's human name
    approx_nanoseconds: float  # => co-16: a widely-cited ORDER-OF-MAGNITUDE figure, not a precise spec number


# ex-27: figures are the well-known "latency numbers every programmer should know" order of
# magnitude (register ~ sub-nanosecond; L1 ~1ns; RAM ~100ns; SSD/disk seek ~10-100 microseconds+) --
# survey depth only, per this topic's co-16 scope note; full treatment in 20-computer-architecture.
HIERARCHY: list[LatencyLevel] = [  # => co-16: ordered FASTEST (closest to the CPU) to SLOWEST (farthest)
    LatencyLevel("register", 0.3),  # => co-16: on-die, accessed in a fraction of one clock cycle
    LatencyLevel("L1 cache", 1.0),  # => co-16: tiny, on-die, one cycle or so
    LatencyLevel("L2 cache", 4.0),  # => co-16: larger, still on-die, a handful of cycles
    LatencyLevel("RAM", 100.0),  # => co-16: off-die -- roughly 100x an L1 hit
    LatencyLevel("SSD", 100_000.0),  # => co-16: a full seek/transfer round trip, not just a bus transaction
    LatencyLevel("HDD (disk)", 10_000_000.0),  # => co-16: a mechanical seek -- the slowest rung surveyed here
]  # => co-16: closes the multi-line construct opened above


if __name__ == "__main__":  # => co-16: entry point -- this block runs only when the file executes directly, not on import
    for level in HIERARCHY:  # => co-16: prints the full ordered survey, level by level
        print(f"{level.name:<12} ~{level.approx_nanoseconds:>12,.1f} ns")  # => co-16: comma-grouped for readability
    latencies = [level.approx_nanoseconds for level in HIERARCHY]  # => co-16: extracted for the ordering check
    is_strictly_increasing = all(  # => co-16: every level must be slower than the one before it
        latencies[i] < latencies[i + 1]
        for i in range(len(latencies) - 1)  # => co-16: adjacent-pair comparison
    )  # => co-16: closes the multi-line construct opened above
    print(f"strictly increasing latency, register -> disk: {is_strictly_increasing}")  # => co-16
    assert is_strictly_increasing, "each hierarchy level must be strictly slower than the previous one"  # => co-16
    print(f"Ordering verified: True")  # => co-16: reached only if the strict-increase assert passed
    # => co-16: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
