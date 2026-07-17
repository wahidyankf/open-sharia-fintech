"""Example 62: pytest verification for Space-Optimized Knapsack DP."""

import random

from example import knapsack_1d_space_optimized, knapsack_2d_full_table


def test_matches_the_full_table_on_random_instances() -> None:
    random.seed(81)
    for _ in range(15):
        n = random.randint(1, 8)
        weights = [random.randint(1, 10) for _ in range(n)]
        values = [random.randint(1, 20) for _ in range(n)]
        capacity = random.randint(1, 20)
        full = knapsack_2d_full_table(weights, values, capacity)
        optimized = knapsack_1d_space_optimized(weights, values, capacity)
        assert full == optimized


def test_zero_capacity_yields_zero_both_ways() -> None:
    assert knapsack_2d_full_table([1, 2], [10, 20], 0) == 0
    assert knapsack_1d_space_optimized([1, 2], [10, 20], 0) == 0


# => Run: pytest -- Output: 2 passed
