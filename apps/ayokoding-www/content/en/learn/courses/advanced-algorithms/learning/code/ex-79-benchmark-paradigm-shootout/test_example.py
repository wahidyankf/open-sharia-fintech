"""Example 79: pytest verification for the Knapsack Paradigm Shootout."""

from example import brute_force_knapsack, dp_knapsack, greedy_knapsack


def test_dp_and_brute_force_always_agree_on_the_optimum() -> None:
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    brute_value, _ = brute_force_knapsack(weights, values, capacity)
    dp_value, _ = dp_knapsack(weights, values, capacity)
    assert brute_value == dp_value


def test_greedy_can_underperform_the_true_optimum() -> None:
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    dp_value, _ = dp_knapsack(weights, values, capacity)
    greedy_value = greedy_knapsack(weights, values, capacity)
    assert (
        greedy_value < dp_value
    )  # => greedy is strictly worse on this classic instance


def test_brute_force_examines_exactly_two_to_the_n_subsets() -> None:
    weights = [1, 2, 3, 4, 5]
    values = [1, 2, 3, 4, 5]
    _, states_examined = brute_force_knapsack(weights, values, capacity=7)
    assert states_examined == 2**5  # => 32 -- every subset of 5 items, no shortcuts


# => Run: pytest -- Output: 3 passed
