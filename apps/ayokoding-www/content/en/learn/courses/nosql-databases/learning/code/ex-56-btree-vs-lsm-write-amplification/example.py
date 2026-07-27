"""Example 56: B-Tree vs. LSM Write Amplification."""  # => co-25: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

PAGE_SIZE_BYTES = 4096  # => co-25: a typical B-tree page size -- an in-place update rewrites the WHOLE page it lives on
RECORD_SIZE_BYTES = 100  # => a representative small record size for this simulation
UPDATES_BATCHED_PER_PAGE = 10  # => co-25: a busy B-tree page absorbs several updates before it is evicted/flushed, amortizing the page-rewrite cost
COMPACTION_LEVELS = 6  # => co-25: an LSM tree's leveled compaction re-writes data once per level as it cascades from L0 down to Lmax


def btree_write_amplification() -> float:  # => co-25: the B-TREE's own LIFETIME amplification, amortized over batched updates per page
    """Return simulated B-tree write amplification, amortized across UPDATES_BATCHED_PER_PAGE per page write."""  # => documents contract
    logical_bytes_per_page_write = UPDATES_BATCHED_PER_PAGE * RECORD_SIZE_BYTES  # => co-25: the LOGICAL bytes served by one page rewrite
    return PAGE_SIZE_BYTES / logical_bytes_per_page_write  # => co-25: PHYSICAL bytes written / LOGICAL bytes served, per page


def lsm_write_amplification() -> float:  # => co-25: the LSM tree's own LIFETIME amplification, from cascading compaction
    """Return simulated LSM write amplification, one full rewrite pass per compaction level."""  # => documents the contract
    return float(COMPACTION_LEVELS)  # => co-25: each level compacts (re-writes) the data it merges -- a simplified but directionally correct model


def raw_write_cost_bytes(engine: str) -> int:  # => co-25: the cost of ONE write, at the instant the client issues it
    """Return the immediate physical write cost (bytes) for a single logical write, per engine."""  # => documents the contract
    if engine == "btree":  # => co-25: a random-I/O, read-modify-write page rewrite, even for a single small record change
        return PAGE_SIZE_BYTES
    return RECORD_SIZE_BYTES  # => co-25: an LSM append is a cheap, sequential write -- no read-modify-write on the critical path


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    btree_amp = btree_write_amplification()  # => co-25: B-tree's LIFETIME write amplification, amortized
    lsm_amp = lsm_write_amplification()  # => co-25: LSM's LIFETIME write amplification, from compaction
    print(f"B-tree write amplification (lifetime, amortized): {btree_amp:.2f}x")  # => Output: B-tree write amplification (lifetime, amortized): 4.10x
    print(f"LSM write amplification (lifetime, compaction):   {lsm_amp:.2f}x")  # => Output: LSM write amplification (lifetime, compaction):   6.00x
    assert lsm_amp > btree_amp  # => co-25: LSM's LIFETIME amplification is HIGHER -- cascading compaction re-writes data more times over its life

    btree_cost = raw_write_cost_bytes("btree")  # => co-25: B-tree's per-write, at-the-moment-of-write cost
    lsm_cost = raw_write_cost_bytes("lsm")  # => co-25: LSM's per-write, at-the-moment-of-write cost
    print(f"B-tree raw cost per write (random I/O, page rewrite): {btree_cost} bytes")  # => Output: B-tree raw cost per write (random I/O, page rewrite): 4096 bytes
    print(f"LSM raw cost per write (sequential append):           {lsm_cost} bytes")  # => Output: LSM raw cost per write (sequential append):           100 bytes
    assert lsm_cost < btree_cost  # => co-25: LSM's PER-WRITE cost is LOWER -- this is what gives it higher RAW write throughput

    print("LSM: higher lifetime write amplification (compaction bill paid later), but higher raw write throughput (cheap sequential appends now)")  # => Output line
    # => co-25: these are TWO DIFFERENT axes, not opposites of the same number -- an LSM tree defers
    # => cost from the write's own critical path into a LATER, background compaction process, which is
    # => exactly why it sustains higher write throughput up front at the cost of paying more, total,
    # => over the data's full lifetime


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
