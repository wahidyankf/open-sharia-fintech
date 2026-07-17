"""Example 29: pytest verification for Closest Pair Divide and Conquer."""

import random

from example import brute_force_closest_pair, closest_pair_divide_conquer


def test_matches_brute_force_on_random_points() -> None:
    random.seed(31)
    points = [
        (random.randint(0, 200), random.randint(0, 200)) for _ in range(40)
    ]  # => 40 random 2D points
    assert closest_pair_divide_conquer(points) == brute_force_closest_pair(points)


def test_matches_brute_force_on_a_small_collinear_set() -> None:
    points = [(0, 0), (1, 0), (5, 0), (9, 0)]  # => all on one line -- an edge shape
    assert closest_pair_divide_conquer(points) == brute_force_closest_pair(points)


# => Run: pytest -- Output: 2 passed
