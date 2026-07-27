"""Example 26: LSM Tombstone Delete."""

# A delete under LSM does not remove bytes in place -- it writes a TOMBSTONE
# marker that shadows older versions the same way a normal write would
# (co-12); the key is truly gone only once compaction later drops the
# tombstone and everything it shadows.
TOMBSTONE = object()  # => a unique sentinel value meaning "deleted here"

memtable: dict[str, object] = {}  # => empty at the start -- nothing written yet
sstable_older: dict[str, object] = {
    "k": "old-value"
}  # => an older, already-flushed segment


def put(
    key: str, value: str
) -> None:  # => an ordinary write, no different from ex-23's memtable_put
    memtable[key] = value


def delete(key: str) -> None:  # => writes a tombstone -- NOT a dict.pop()
    memtable[key] = (
        TOMBSTONE  # => a real entry whose VALUE means "deleted", not an absent key
    )


def lsm_get(
    key: str,
) -> str | None:  # => same newest-first read path as ex-25, tombstone-aware
    if key in memtable:
        value = memtable[key]
        return (
            None if value is TOMBSTONE else str(value)
        )  # => a tombstone means "not found", not an error
    if key in sstable_older:
        return str(sstable_older[key])
    return None


print(lsm_get("k"))  # => Output: old-value
# => before the delete, the read falls through to the older sstable and finds a value
delete(
    "k"
)  # => writes a tombstone into the memtable, shadowing the older sstable value
print(lsm_get("k"))  # => Output: None
# => after the delete, the tombstone shadows the sstable value the same way a write would

assert lsm_get("k") is None  # => a read after the tombstone reports not-found
assert (
    memtable["k"] is TOMBSTONE
)  # => the tombstone itself is a real, present marker -- not an absence
# => "k" still has a dict entry -- it is present AND resolves to deleted, not simply missing
print("ex-26 OK")  # => Output: ex-26 OK
