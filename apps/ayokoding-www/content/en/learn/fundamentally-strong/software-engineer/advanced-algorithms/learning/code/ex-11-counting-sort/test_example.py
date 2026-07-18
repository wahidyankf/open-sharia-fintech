"""Example 11: pytest verification for Counting Sort."""

import random

from example import counting_sort


def test_matches_builtin_sorted_on_random_bounded_input() -> None:
    random.seed(9)
    data: list[int] = [random.randint(0, 99) for _ in range(80)]  # => range 0..99
    assert counting_sort(data, k=100) == sorted(data)


def test_preserves_relative_order_of_equal_keys_when_stable() -> None:
    data: list[int] = [3, 1, 3, 1, 2]
    assert counting_sort(data, k=4) == [1, 1, 2, 3, 3]  # => all duplicates present


# => Run: pytest -- Output: 2 passed
