"""Example 25: pytest verification for the LSM Read Path (Newest Wins)."""

from example import lsm_get, memtable, sstables_newest_first


def test_memtable_shadows_all_sstables() -> None:
    assert lsm_get("x") == memtable["x"]


def test_newer_sstable_shadows_older_sstable() -> None:
    assert lsm_get("y") == sstables_newest_first[0]["y"]


# => Run: pytest -- Output: 2 passed
