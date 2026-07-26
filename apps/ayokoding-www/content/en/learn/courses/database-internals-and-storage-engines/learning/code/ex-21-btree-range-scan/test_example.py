"""Example 21: pytest verification for B-Tree Range Scan via Sibling Links."""

from example import Leaf, range_scan


def test_range_scan_spans_multiple_leaves() -> None:
    leaf_a = Leaf(keys=[1, 2, 3])
    leaf_b = Leaf(keys=[4, 5, 6])
    leaf_a.next = leaf_b
    assert range_scan(leaf_a, 2, 5) == [2, 3, 4, 5]


def test_range_scan_stops_once_past_hi() -> None:
    leaf_a = Leaf(keys=[1, 2, 3])
    leaf_b = Leaf(keys=[100, 200])
    leaf_a.next = leaf_b
    assert range_scan(leaf_a, 1, 3) == [1, 2, 3]  # => never even reads leaf_b's keys


# => Run: pytest -- Output: 2 passed
