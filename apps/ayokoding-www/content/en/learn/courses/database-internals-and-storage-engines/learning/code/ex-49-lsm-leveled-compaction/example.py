"""Example 49: LSM Leveled Compaction."""
# Leveled compaction (co-13) guarantees NO key-range overlap between tables within one level.

from dataclasses import dataclass  # => a typed SSTable with an explicit key range


@dataclass  # => a plain, typed record -- no custom __init__ needed
class SSTable:  # => a sorted, immutable segment, tagged with its own key range
    data: dict[str, str]  # => key -> value, sorted by key on disk
    min_key: str  # => the smallest key this table contains -- used to detect overlap
    max_key: str  # => the largest key this table contains -- used to detect overlap


def overlaps(
    a: SSTable, b: SSTable
) -> bool:  # => do two tables' key ranges intersect at all?
    return (
        a.min_key <= b.max_key and b.min_key <= a.max_key
    )  # => standard interval-overlap test


def push_down(
    incoming: SSTable, level: list[SSTable]
) -> list[SSTable]:  # => co-13: merge overlaps away
    overlapping = [
        t for t in level if overlaps(incoming, t)
    ]  # => every existing table this one touches
    non_overlapping = [
        t for t in level if t not in overlapping
    ]  # => tables entirely untouched by the push
    merged_data: dict[
        str, str
    ] = {}  # => the combined contents of the incoming table and its overlaps
    for (
        table
    ) in overlapping:  # => older tables in this level, oldest key precedence first
        merged_data.update(table.data)  # => start from what was already in the level
    merged_data.update(
        incoming.data
    )  # => the incoming (newer) table's keys win any conflicts
    keys = sorted(
        merged_data
    )  # => the merged key range, sorted, needed for min/max below
    merged = SSTable(
        data=merged_data, min_key=keys[0], max_key=keys[-1]
    )  # => one new, overlap-free table
    return non_overlapping + [
        merged
    ]  # => the level after the push: untouched tables plus the merged one


level = [  # => two disjoint existing tables in this level
    SSTable(
        data={"a": "v1", "b": "v1"}, min_key="a", max_key="b"
    ),  # => an existing table in this level
    SSTable(
        data={"m": "v1", "n": "v1"}, min_key="m", max_key="n"
    ),  # => a DISJOINT existing table
]  # => end of the level fixture
incoming = SSTable(
    data={"b": "v2", "c": "v1"}, min_key="b", max_key="c"
)  # => overlaps the first table

new_level = push_down(incoming, level)  # => run leveled compaction's push-down step
print(len(new_level))  # => Output: 2

for i, table_a in enumerate(
    new_level
):  # => check EVERY pair of tables in the resulting level
    for table_b in new_level[
        i + 1 :
    ]:  # => compare each table only against the ones after it
        assert not overlaps(
            table_a, table_b
        )  # => no two tables in the level may share any key range
print("ex-49 OK")  # => Output: ex-49 OK
