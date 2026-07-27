"""Worked Example 25: Per-Partition Ordering, Not Global."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def interleave(partition_0: list[str], partition_1: list[str]) -> list[str]:  # => co-13: simulates records arriving from TWO partitions, interleaved
    """Interleave two partitions' records as a consumer might actually observe them arriving."""  # => co-13: documents interleave's contract -- no runtime output, just sets its __doc__
    interleaved: list[str] = []  # => co-13: the observed ARRIVAL order across both partitions combined
    for a, b in zip(partition_0, partition_1):  # => co-13: alternate one record from each partition, simulating real-world interleaving
        interleaved.append(a)  # => co-13: partition 0's next record
        interleaved.append(b)  # => co-13: partition 1's next record, interleaved with partition 0's
    return interleaved  # => co-13: returns this computed value to the caller


if __name__ == "__main__":  # => co-13: entry point -- runs only when this file executes directly, not on import
    partition_0 = ["p0-msg-1", "p0-msg-2", "p0-msg-3"]  # => co-13: partition 0's OWN internal order -- 1, 2, 3
    partition_1 = ["p1-msg-1", "p1-msg-2", "p1-msg-3"]  # => co-13: partition 1's OWN internal order -- 1, 2, 3, independent of partition 0
    observed_order = interleave(partition_0, partition_1)  # => co-13: what a consumer subscribed to BOTH partitions actually sees
    print(f"Observed arrival order (both partitions interleaved): {observed_order}")  # => co-13: prints the interleaved sequence

    partition_0_positions = [observed_order.index(msg) for msg in partition_0]  # => co-13: WHERE each partition-0 message landed in the interleaved stream
    partition_0_order_preserved = partition_0_positions == sorted(partition_0_positions)  # => co-13: partition 0's OWN messages stay in relative order
    print(f"Partition 0's own messages stay in relative order: {partition_0_order_preserved}")  # => co-13: prints the within-partition check

    cross_partition_order_meaningless = observed_order[0] != "p0-msg-1" or observed_order[1] != "p1-msg-1"  # => co-13: whichever came "first" here is arbitrary interleaving
    global_order_across_partitions = observed_order  # => co-13: there is no single global sequence number spanning both partitions at all
    print(f"No single global offset spans both partitions: {len(set(len(p) for p in (partition_0, partition_1))) == 1}")  # => co-13
    assert partition_0_order_preserved, "within one partition, order must be preserved exactly"  # => co-13: the claim ex-25 makes
    assert observed_order != partition_0 + partition_1, "across partitions, the interleaving is NOT a simple partition-by-partition sequence"  # => co-13
    print("MATCH: order holds strictly WITHIN each partition; ACROSS partitions, only interleaved arrival order exists")  # => co-13
    # => co-13: "ordering is guaranteed only within a partition" is why a producer keys related records to the SAME partition
