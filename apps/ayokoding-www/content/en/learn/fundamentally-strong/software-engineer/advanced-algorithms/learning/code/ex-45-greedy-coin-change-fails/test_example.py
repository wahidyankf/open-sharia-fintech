"""Example 45: pytest verification for Greedy Coin Change's Failure Case."""

from example import greedy_coin_change


def test_greedy_produces_valid_but_suboptimal_change() -> None:
    result = greedy_coin_change([1, 3, 4], 6)
    assert sum(result) == 6  # => still valid change...
    assert len(result) == 3  # => ...but not the minimum possible (2, via 3+3)


def test_greedy_is_optimal_on_us_coin_denominations() -> None:
    result = greedy_coin_change([1, 5, 10, 25], 41)
    assert sum(result) == 41
    assert len(result) == 4  # => 25 + 10 + 5 + 1 -- greedy IS optimal for these coins


# => Run: pytest -- Output: 2 passed
