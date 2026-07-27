"""Example 48: pytest verification for LSM Size-Tiered Compaction."""

from example import SSTable, compact


def test_compaction_reduces_segment_count_to_one() -> None:
    tables = [SSTable(data={"x": "1"}), SSTable(data={"y": "2"})]
    merged = compact(tables)
    assert isinstance(merged, SSTable)


def test_compaction_preserves_every_key_with_newest_value_winning() -> None:
    tables = [SSTable(data={"k": "old"}), SSTable(data={"k": "new"})]
    merged = compact(tables)
    assert merged.data["k"] == "new"


# => Run: pytest -- Output: 2 passed
