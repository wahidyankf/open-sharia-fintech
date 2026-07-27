"""Example 26: pytest verification for the LSM Tombstone Delete."""

from example import TOMBSTONE, delete, lsm_get, memtable, put


def test_read_after_tombstone_is_not_found() -> None:
    memtable.clear()
    put("k", "v")
    delete("k")
    assert lsm_get("k") is None


def test_tombstone_is_a_real_marker_not_a_removal() -> None:
    memtable.clear()
    delete("k")
    assert (
        memtable["k"] is TOMBSTONE
    )  # => the key still has an ENTRY -- it just resolves to "deleted"


# => Run: pytest -- Output: 2 passed
