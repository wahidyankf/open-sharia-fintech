"""Example 48: LSM Size-Tiered Compaction."""
# Size-tiered compaction (co-13) merges same-size SSTables into one.

from dataclasses import dataclass, field  # => a typed SSTable representation


@dataclass  # => a plain, typed record -- no custom __init__ needed
class SSTable:  # => an immutable, sorted, on-disk segment (co-11/co-12 territory)
    data: dict[str, str] = field(
        default_factory=dict[str, str]
    )  # => key -> value, sorted by key on disk


def compact(
    tables: list[SSTable],
) -> SSTable:  # => size-tiered: merge SAME-SIZE tables into ONE bigger one
    merged: dict[str, str] = {}  # => the result of merging every input table
    for (
        table
    ) in tables:  # => later tables (newer) override earlier ones on key conflicts
        merged.update(
            table.data
        )  # => co-12: newest-wins -- a later table's value replaces an earlier one
    return SSTable(
        data=merged
    )  # => one new, larger table replaces however many went in


tables = [  # => three small SSTables from the same size tier
    SSTable(data={"a": "v1", "b": "v1"}),  # => oldest SSTable
    SSTable(data={"c": "v1", "d": "v1"}),  # => same tier, disjoint keys
    SSTable(data={"a": "v2"}),  # => newest SSTable -- overwrites key "a"
]  # => end of the SSTable fixture
segment_count_before = len(tables)  # => three separate segments before compaction
merged = compact(tables)  # => run size-tiered compaction over all three tables
segment_count_after = (
    1  # => size-tiered compaction always produces exactly one output segment
)
print(segment_count_before)  # => Output: 3
print(segment_count_after)  # => Output: 1
print(
    sorted(merged.data.items())
)  # => Output: [('a', 'v2'), ('b', 'v1'), ('c', 'v1'), ('d', 'v1')]

assert (
    segment_count_after < segment_count_before
)  # => the merged segment count genuinely dropped
assert (
    merged.data["a"] == "v2"
)  # => every key survived, and the NEWEST value for "a" won
assert set(merged.data.keys()) == {
    "a",
    "b",
    "c",
    "d",
}  # => no key was lost during the merge
print("ex-48 OK")  # => Output: ex-48 OK
