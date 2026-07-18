"""Example 30: pytest verification for the Fenwick Tree."""

import random

from example import FenwickTree


def test_matches_a_running_array_after_random_updates() -> None:
    random.seed(41)
    n = 30
    running: list[int] = [0] * n
    fenwick = FenwickTree(n)
    for _ in range(100):  # => 100 random point updates
        idx = random.randint(0, n - 1)
        delta = random.randint(-5, 5)
        fenwick.update(idx, delta)
        running[idx] += delta
        lo = random.randint(0, n - 1)
        hi = random.randint(lo, n - 1)
        assert fenwick.range_sum(lo, hi) == sum(running[lo : hi + 1])


def test_prefix_sum_of_all_zeros_is_zero() -> None:
    fenwick = FenwickTree(5)
    assert fenwick.prefix_sum(4) == 0  # => nothing has been added yet


# => Run: pytest -- Output: 2 passed
