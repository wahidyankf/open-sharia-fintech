"""pytest coverage for index.py -- the B+-tree-style index over page ids."""

from index import BTreeIndex


def test_a_point_lookup_finds_an_inserted_key() -> None:
    index = BTreeIndex()
    index.insert(5, page_id=50)
    assert index.lookup(5) == 50


def test_a_point_lookup_for_a_missing_key_returns_none() -> None:
    index = BTreeIndex()
    index.insert(5, page_id=50)
    assert index.lookup(99) is None


def test_insertion_order_does_not_affect_lookup_correctness() -> None:
    index = BTreeIndex()
    for key in [9, 1, 5, 3, 7]:
        index.insert(key, page_id=key * 100)
    for key in [9, 1, 5, 3, 7]:
        assert index.lookup(key) == key * 100


def test_a_range_scan_returns_only_keys_inside_the_bounds_in_sorted_order() -> None:
    index = BTreeIndex()
    for key in [10, 2, 6, 8, 4]:
        index.insert(key, page_id=key)
    assert index.range_scan(4, 8) == [(4, 4), (6, 6), (8, 8)]


def test_a_leaf_that_overflows_capacity_splits_without_losing_any_key() -> None:
    index = BTreeIndex()
    for key in range(20):  # => far more keys than one leaf's LEAF_CAPACITY can hold
        index.insert(key, page_id=key)
    assert len(index.leaves) > 1  # => the overflow forced at least one split
    for key in range(20):  # => every key must still be findable after every split
        assert index.lookup(key) == key


def test_re_inserting_an_existing_key_updates_its_pointer_in_place() -> None:
    index = BTreeIndex()
    index.insert(1, page_id=100)  # => key 1 first points at page 100
    index.insert(
        1, page_id=200
    )  # => a later update -- must REPLACE, not duplicate, the entry
    assert index.lookup(1) == 200  # => the pointer now reflects the newest write
    assert (
        sum(1 for leaf in index.leaves for k, _ in leaf if k == 1) == 1
    )  # => exactly one entry for key 1


# => Run: pytest -- Output: 6 passed
