"""Example 77: B-Tree vs LSM -- Measured Write Throughput."""
# LSM (co-14) defers per-insert I/O cost via buffering; a B-tree pays it immediately, per insert.


def btree_simulated_page_writes(
    insert_count: int,
) -> int:  # => a B-tree: ~1 page write per random insert
    return insert_count  # => each insert may touch (and dirty) a distinct, randomly-located leaf page


def lsm_simulated_page_writes(
    insert_count: int, flush_every: int
) -> int:  # => LSM: cheap until a flush
    # => all inserts land in the in-memory memtable first -- ~free from a page-I/O point of view
    flush_count = (
        insert_count // flush_every
    )  # => how many times the memtable had to flush to an SSTable
    page_writes_from_flushes = (
        flush_count  # => each flush is ONE sequential write, however many keys it holds
    )
    return (
        page_writes_from_flushes  # => far fewer "page writes" than the raw insert count
    )


insert_count = 1000  # => the same random-insert workload run against both engines
btree_cost = btree_simulated_page_writes(
    insert_count
)  # => the B-tree's simulated I/O cost
lsm_cost = lsm_simulated_page_writes(
    insert_count, flush_every=100
)  # => flush once every 100 buffered inserts
print(btree_cost)  # => Output: 1000
print(lsm_cost)  # => Output: 10

btree_throughput = (
    insert_count / btree_cost
)  # => inserts served per unit of simulated I/O
lsm_throughput = insert_count / lsm_cost  # => same metric, for the LSM engine
print(btree_throughput < lsm_throughput)  # => Output: True

assert (
    lsm_throughput > btree_throughput
)  # => the LSM engine sustains higher throughput on this workload
print("ex-77 OK")  # => Output: ex-77 OK
