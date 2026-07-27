"""Example 43: pytest verification for B-Tree Bulk Load vs Insert-One-by-One."""

from example import bulk_load, insert_one, lookup


def test_bulk_and_incremental_agree_on_every_lookup() -> None:
    sorted_keys = list(range(0, 12, 2))
    bulk_leaves = bulk_load(sorted_keys, capacity=4)
    incremental_leaves: list[list[int]] = []
    for key in sorted_keys:
        insert_one(incremental_leaves, key, capacity=4)
    for probe in sorted_keys + [1, 99]:
        assert lookup(bulk_leaves, probe) == lookup(incremental_leaves, probe)


def test_absent_key_is_not_found_in_either_structure() -> None:
    bulk_leaves = bulk_load([0, 2, 4], capacity=4)
    assert lookup(bulk_leaves, 3) is False


# => Run: pytest -- Output: 2 passed
