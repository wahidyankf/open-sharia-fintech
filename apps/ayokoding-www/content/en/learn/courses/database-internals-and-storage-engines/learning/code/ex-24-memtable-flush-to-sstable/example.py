"""Example 24: Flush a Memtable to an SSTable."""

# Once a memtable grows past a size threshold, it is flushed to disk as an
# IMMUTABLE, sorted SSTable, and a fresh empty memtable takes over writes
# (co-11) -- "immutable" is the key word: an SSTable is never edited again,
# only replaced by a later compaction.


def flush(
    memtable: list[tuple[str, str]],
) -> list[tuple[str, str]]:  # => returns a NEW sorted SSTable
    sstable = sorted(
        memtable, key=lambda pair: pair[0]
    )  # => sort once, at flush time, not on every write
    memtable.clear()  # => the memtable is now empty and ready for new writes
    return sstable


memtable: list[tuple[str, str]] = [("bob", "2"), ("alice", "1"), ("charlie", "3")]
sstable = flush(memtable)
print(sstable)  # => Output: [('alice', '1'), ('bob', '2'), ('charlie', '3')]
print(memtable)  # => Output: []

assert sstable == sorted(sstable)  # => the flushed segment is sorted by key
assert (
    memtable == []
)  # => the memtable was cleared -- future writes go into a fresh one
print("ex-24 OK")  # => Output: ex-24 OK
