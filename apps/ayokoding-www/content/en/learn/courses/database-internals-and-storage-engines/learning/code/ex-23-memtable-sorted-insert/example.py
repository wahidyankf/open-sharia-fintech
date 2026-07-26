"""Example 23: Memtable -- Sorted Insert."""

import bisect  # => stdlib module used to find each new key's correct sorted position

# An LSM engine buffers every write in an in-memory SORTED structure -- the
# memtable -- before anything touches disk (co-11). RocksDB's default
# memtable implementation is a skiplist; this example models the same
# "always sorted" contract with a plain list kept sorted via bisect.
memtable: list[tuple[str, str]] = []  # => (key, value) pairs, kept sorted BY KEY


def memtable_put(
    key: str, value: str
) -> None:  # => insert, or overwrite an existing key in place
    keys = [
        k for k, _ in memtable
    ]  # => extract just the keys to find the insertion point
    i = bisect.bisect_left(
        keys, key
    )  # => O(log n) to FIND the position; the list insert itself is O(n)
    if (
        i < len(memtable) and memtable[i][0] == key
    ):  # => key already present: overwrite in place
        memtable[i] = (key, value)
    else:
        memtable.insert(i, (key, value))  # => new key: insert at the sorted position


for k, v in [
    ("charlie", "3"),
    ("alice", "1"),
    ("bob", "2"),
]:  # => inserted out of order
    memtable_put(k, v)
print(memtable)  # => Output: [('alice', '1'), ('bob', '2'), ('charlie', '3')]

assert [k for k, _ in memtable] == [
    "alice",
    "bob",
    "charlie",
]  # => iteration is ALWAYS in sorted-key order
print("ex-23 OK")  # => Output: ex-23 OK
