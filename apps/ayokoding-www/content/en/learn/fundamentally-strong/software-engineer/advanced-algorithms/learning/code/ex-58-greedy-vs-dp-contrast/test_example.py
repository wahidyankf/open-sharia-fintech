"""Example 58: pytest verification for Greedy vs DP on 0/1 Knapsack."""

from example import greedy_knapsack_by_ratio, knapsack_01_dp


def test_dp_strictly_beats_ratio_greedy_on_the_classic_counterexample() -> None:
    weights, values, capacity = [10, 20, 30], [60, 100, 120], 50
    greedy = greedy_knapsack_by_ratio(weights, values, capacity)
    optimal = knapsack_01_dp(weights, values, capacity)
    assert greedy == 160
    assert optimal == 220
    assert optimal > greedy


def test_both_agree_when_all_items_fit_anyway() -> None:
    weights, values, capacity = [1, 2, 3], [10, 20, 30], 100  # => everything fits
    assert greedy_knapsack_by_ratio(weights, values, capacity) == knapsack_01_dp(
        weights, values, capacity
    )


# => Run: pytest -- Output: 2 passed
