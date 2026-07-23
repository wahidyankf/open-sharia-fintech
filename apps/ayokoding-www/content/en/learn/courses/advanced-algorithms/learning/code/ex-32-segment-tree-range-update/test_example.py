"""Example 32: pytest verification for Lazy Range-Add Segment Tree."""

import random

from example import LazySegmentTree


def test_matches_a_brute_force_running_array_after_random_range_adds() -> None:
    random.seed(61)
    n = 20
    running: list[int] = [0] * n
    tree = LazySegmentTree(running)
    for _ in range(50):  # => 50 random overlapping range-add operations
        lo = random.randint(0, n - 1)
        hi = random.randint(lo, n - 1)
        delta = random.randint(-10, 10)
        tree.range_add(lo, hi, delta)
        for i in range(lo, hi + 1):  # => the brute-force ground truth, applied directly
            running[i] += delta
        for i in range(n):  # => re-checks every index after each update
            assert tree.point_query(i) == running[i]


def test_non_overlapping_updates_stay_independent() -> None:
    tree = LazySegmentTree([0, 0, 0, 0])
    tree.range_add(0, 1, 5)
    tree.range_add(2, 3, -3)
    assert [tree.point_query(i) for i in range(4)] == [5, 5, -3, -3]


# => Run: pytest -- Output: 2 passed
