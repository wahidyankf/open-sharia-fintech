"""Example 31: pytest verification for Segment Tree Range-Min."""

import random

from example import SegmentTreeMin


def test_matches_brute_force_slice_min_on_random_ranges() -> None:
    random.seed(51)
    data = [random.randint(-50, 50) for _ in range(25)]
    tree = SegmentTreeMin(data)
    for _ in range(60):
        lo = random.randint(0, len(data) - 1)
        hi = random.randint(lo, len(data) - 1)
        assert tree.query(lo, hi) == min(data[lo : hi + 1])


def test_whole_array_query_matches_python_min() -> None:
    data = [4, -2, 9, 0, 7]
    tree = SegmentTreeMin(data)
    assert tree.query(0, len(data) - 1) == min(data)


# => Run: pytest -- Output: 2 passed
