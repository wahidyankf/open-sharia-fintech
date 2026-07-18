"""Example 67: pytest verification for Segment Tree vs Fenwick Tree."""

import random

from example import FenwickTree, SegmentTreeSum


def test_both_structures_agree_after_random_updates() -> None:
    random.seed(101)
    n = 25
    fenwick = FenwickTree(n)
    segment_tree = SegmentTreeSum(n)
    for _ in range(60):
        idx = random.randint(0, n - 1)
        delta = random.randint(-10, 10)
        fenwick.update(idx, delta)
        segment_tree.update(idx, delta)
        q = random.randint(0, n - 1)
        assert fenwick.prefix_sum(q) == segment_tree.prefix_sum(q)


def test_fenwick_space_is_smaller_than_segment_tree_space() -> None:
    n = 50
    fenwick = FenwickTree(n)
    segment_tree = SegmentTreeSum(n)
    assert len(fenwick.tree) < len(segment_tree.tree)


# => Run: pytest -- Output: 2 passed
