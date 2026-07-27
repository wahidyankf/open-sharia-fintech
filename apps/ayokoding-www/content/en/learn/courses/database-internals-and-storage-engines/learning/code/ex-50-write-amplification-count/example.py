"""Example 50: Count Write Amplification."""
# Write amplification (co-14) is bytes ACTUALLY written to disk / bytes the application asked to write.

application_bytes = 0  # => the true, logical amount of data the application wrote
disk_bytes_written = (
    0  # => every byte ACTUALLY written to storage, across every compaction pass
)


def flush_memtable(
    data: dict[str, str],
) -> None:  # => the memtable's first write to disk (a new SSTable)
    global application_bytes, disk_bytes_written  # => mutate both module-level counters
    size = sum(
        len(k) + len(v) for k, v in data.items()
    )  # => rough byte size of this batch
    application_bytes += size  # => this many bytes came from the application itself
    disk_bytes_written += size  # => the FIRST write of these bytes to disk


def compact(
    tables: list[dict[str, str]],
) -> dict[str, str]:  # => merges N tables, REWRITING every byte
    global disk_bytes_written  # => this counter grows on EVERY compaction, not just the first flush
    merged: dict[str, str] = {}  # => the compacted result -- newest table's values win
    for table in tables:  # => later tables' values win on key conflicts
        merged.update(
            table
        )  # => later tables in the list override earlier ones on conflict
    size = sum(
        len(k) + len(v) for k, v in merged.items()
    )  # => the merged table's own byte size
    disk_bytes_written += (
        size  # => compaction WRITES these bytes again -- this is the amplification
    )
    return merged  # => hand back the merged table for the next compaction round, if any


flush_memtable(
    {"a": "v1", "b": "v1"}
)  # => first flush -- application writes these bytes once
flush_memtable({"c": "v1"})  # => second flush -- more application bytes
table1 = {"a": "v1", "b": "v1"}  # => a plain dict standing in for a flushed SSTable
table2 = {"c": "v1"}  # => a second flushed SSTable, disjoint keys from table1
merged = compact(
    [table1, table2]
)  # => compaction #1 rewrites everything flushed so far
merged = compact(
    [merged, {"a": "v2"}]
)  # => compaction #2 rewrites it AGAIN, plus a new update

amplification = (
    disk_bytes_written / application_bytes
)  # => the exact ratio the spec asks to verify
print(application_bytes)  # => Output: 9
print(disk_bytes_written)  # => Output: 27
print(round(amplification, 2))  # => Output: 3.0

assert (
    amplification > 1
)  # => compaction rewrote bytes multiple times -- more disk I/O than logical writes
print("ex-50 OK")  # => Output: ex-50 OK
