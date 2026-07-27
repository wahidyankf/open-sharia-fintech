"""Example 52: pytest verification for Space Amplification Measurement."""

from example import SSTable, live_bytes, on_disk_bytes


def test_space_amplification_exceeds_one_with_stale_versions() -> None:
    tables = [SSTable(data={"k": "old"}), SSTable(data={"k": "new"})]
    assert on_disk_bytes(tables) / live_bytes(tables) > 1


def test_no_stale_versions_gives_amplification_of_exactly_one() -> None:
    tables = [SSTable(data={"a": "1"}), SSTable(data={"b": "2"})]
    assert on_disk_bytes(tables) == live_bytes(tables)


# => Run: pytest -- Output: 2 passed
