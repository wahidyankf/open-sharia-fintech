"""Example 60: pytest verification for Longest Increasing Subsequence."""

import random

from example import lis_length_dp, lis_length_patience


def test_both_approaches_agree_on_random_sequences() -> None:
    random.seed(71)
    for _ in range(20):
        seq = [random.randint(0, 30) for _ in range(15)]
        assert lis_length_dp(seq) == lis_length_patience(seq)


def test_strictly_increasing_input_has_lis_equal_to_its_own_length() -> None:
    seq = [1, 2, 3, 4, 5]
    assert lis_length_dp(seq) == 5
    assert lis_length_patience(seq) == 5


def test_strictly_decreasing_input_has_lis_of_one() -> None:
    seq = [5, 4, 3, 2, 1]
    assert lis_length_dp(seq) == 1
    assert lis_length_patience(seq) == 1


# => Run: pytest -- Output: 3 passed
