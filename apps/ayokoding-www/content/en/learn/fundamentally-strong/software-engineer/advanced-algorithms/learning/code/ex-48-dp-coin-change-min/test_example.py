"""Example 48: pytest verification for DP Minimum Coin Change."""

from example import min_coins_dp


def test_beats_the_greedy_answer_on_the_non_canonical_coin_set() -> None:
    assert min_coins_dp([1, 3, 4], 6) == 2  # => strictly fewer than greedy's 3


def test_us_coins_matches_greedy_since_greedy_is_optimal_there() -> None:
    assert min_coins_dp([1, 5, 10, 25], 41) == 4


def test_unreachable_amount_returns_none() -> None:
    assert min_coins_dp([5], 3) is None


# => Run: pytest -- Output: 3 passed
