"""Example 78: B-Tree vs LSM -- Measured Read Latency."""
# A B-tree's read cost (co-14) is bounded by height; an LSM's grows with un-compacted segment count.

import math  # => stdlib log/ceil, matching ex-19's height formula


def btree_simulated_page_reads(
    key_count: int, fanout: int
) -> int:  # => co-08: height ~= log_fanout(N)
    return (
        math.ceil(math.log(key_count, fanout)) + 1
    )  # => +1 for the leaf level itself, as in ex-19


def lsm_simulated_page_reads(
    sstable_count: int,
) -> int:  # => co-12: newest-to-oldest scan, worst case
    return sstable_count  # => without a Bloom filter (ex-53), a miss checks EVERY un-compacted segment


key_count = 1_000_000  # => a million-key table, read-heavy workload
fanout = 200  # => illustrative fanout, matching this course's own pedagogical (not vendor) numbers
sstable_count = 8  # => an LSM engine that has accumulated 8 un-compacted segments

btree_cost = btree_simulated_page_reads(
    key_count, fanout
)  # => the B-tree's simulated read cost
lsm_cost = lsm_simulated_page_reads(
    sstable_count
)  # => the LSM engine's simulated read cost, same workload
print(btree_cost)  # => Output: 4
print(lsm_cost)  # => Output: 8

assert (
    btree_cost < lsm_cost
)  # => the B-tree answers a point read in fewer simulated page reads here
print("ex-78 OK")  # => Output: ex-78 OK
