"""Example 51: pytest verification for 0/1 Knapsack."""

from example import knapsack_01


def test_matches_a_known_optimal_value() -> None:
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    assert knapsack_01(weights, values, capacity=7) == 9  # => items of weight 3 and 4


def test_zero_capacity_yields_zero_value() -> None:
    assert knapsack_01([1, 2, 3], [10, 20, 30], capacity=0) == 0


def test_single_item_that_exactly_fits() -> None:
    assert knapsack_01([5], [42], capacity=5) == 42


# => Run: pytest -- Output: 3 passed
