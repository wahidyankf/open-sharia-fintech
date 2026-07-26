"""Example 25: LSM Read Path -- Newest Wins."""

# A point read checks the memtable FIRST, then on-disk SSTables from newest
# to oldest, returning the FIRST match found (co-12) -- since a later write
# always shadows an earlier one, "first found while searching newest-first"
# is exactly "most recent value".
memtable: dict[str, str] = {
    "x": "memtable-value"
}  # => the most recent writes, not yet flushed
sstables_newest_first: list[dict[str, str]] = [
    {"x": "sstable-2-value", "y": "y-in-sstable-2"},  # => flushed more recently
    {
        "x": "sstable-1-value",
        "y": "y-in-sstable-1",
    },  # => flushed first, therefore OLDEST
]


def lsm_get(key: str) -> str | None:  # => the full LSM read path in five lines
    if key in memtable:  # => the memtable is always checked before ANY on-disk segment
        return memtable[key]
    for sstable in (
        sstables_newest_first
    ):  # => walk segments newest -> oldest, stop at the first hit
        if (
            key in sstable
        ):  # => the FIRST match found is, by construction, the newest one
            return sstable[key]
    return None  # => absent from the memtable AND every sstable -- genuinely not found


print(lsm_get("x"))  # => Output: memtable-value
print(lsm_get("y"))  # => Output: y-in-sstable-2
# => the OLDER sstable's "y-in-sstable-1" value is never even looked at

assert lsm_get("x") == "memtable-value"  # => memtable shadows BOTH sstables for key x
assert (
    lsm_get("y") == "y-in-sstable-2"
)  # => the newer sstable shadows the older one for key y
print("ex-25 OK")  # => Output: ex-25 OK
