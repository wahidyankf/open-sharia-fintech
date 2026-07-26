"""Example 49: pytest verification for LSM Leveled Compaction."""

from example import SSTable, overlaps, push_down


def test_pushed_down_level_has_no_key_overlap() -> None:
    level = [SSTable(data={"a": "1"}, min_key="a", max_key="a")]
    incoming = SSTable(data={"a": "2", "b": "1"}, min_key="a", max_key="b")
    result = push_down(incoming, level)
    for i, t1 in enumerate(result):
        for t2 in result[i + 1 :]:
            assert not overlaps(t1, t2)


def test_disjoint_incoming_table_stays_separate() -> None:
    level = [SSTable(data={"a": "1"}, min_key="a", max_key="a")]
    incoming = SSTable(data={"z": "1"}, min_key="z", max_key="z")
    result = push_down(incoming, level)
    assert len(result) == 2


# => Run: pytest -- Output: 2 passed
