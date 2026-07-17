"""Example 5: pytest verification for Top-Down Merge Sort."""

import random

from example import merge_sort


def test_matches_builtin_sorted_on_random_input() -> None:
    random.seed(7)
    data: list[int] = random.sample(range(1, 500), 40)  # => 40 distinct random ints
    assert merge_sort(data) == sorted(data)  # => same answer as Python's own sort


def test_empty_and_single_element_edge_cases() -> None:
    assert merge_sort([]) == []  # => sorting nothing yields nothing
    assert merge_sort([9]) == [9]  # => sorting one element yields that element


def test_already_sorted_input_stays_sorted() -> None:
    assert merge_sort([1, 2, 3, 4]) == [1, 2, 3, 4]  # => a sorted input is a no-op


# => Run: pytest -- Output: 3 passed
