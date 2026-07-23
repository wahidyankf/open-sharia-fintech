"""Example 24: pytest verification for Sliding-Window Max Sum."""

import random

from example import brute_force_max_window_sum, sliding_window_max_sum


def test_matches_brute_force_on_random_input() -> None:
    random.seed(21)
    data: list[int] = [
        random.randint(-10, 10) for _ in range(30)
    ]  # => allows negatives
    k = 5
    assert sliding_window_max_sum(data, k) == brute_force_max_window_sum(data, k)


def test_window_equal_to_full_list_length() -> None:
    data: list[int] = [1, 2, 3, 4]
    assert sliding_window_max_sum(data, k=4) == sum(data)  # => only one window exists


# => Run: pytest -- Output: 2 passed
