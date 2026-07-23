"""Example 7: pytest verification for Quicksort with Lomuto Partitioning."""

import random

from example import quicksort


def test_matches_builtin_sorted_on_random_input() -> None:
    random.seed(3)
    data: list[int] = random.sample(range(1, 300), 25)
    expected = sorted(data)
    quicksort(data)  # => sorts data in place
    assert data == expected  # => same final order as Python's own sort


def test_handles_duplicate_values() -> None:
    data: list[int] = [5, 3, 5, 1, 5, 2]  # => repeated pivots exercise ties
    quicksort(data)
    assert data == [1, 2, 3, 5, 5, 5]  # => duplicates land correctly, no data lost


def test_empty_and_single_element_are_no_ops() -> None:
    empty: list[int] = []
    quicksort(empty)
    assert empty == []  # => nothing to sort, nothing changes

    one: list[int] = [42]
    quicksort(one)
    assert one == [42]  # => a single element is trivially sorted


# => Run: pytest -- Output: 3 passed
