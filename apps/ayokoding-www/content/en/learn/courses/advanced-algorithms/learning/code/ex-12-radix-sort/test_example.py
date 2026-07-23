"""Example 12: pytest verification for LSD Radix Sort."""

import random

from example import radix_sort


def test_matches_builtin_sorted_on_random_input() -> None:
    random.seed(13)
    data: list[int] = [random.randint(0, 9999) for _ in range(50)]  # => up to 4 digits
    assert radix_sort(data) == sorted(data)


def test_single_element_and_all_equal_values() -> None:
    assert radix_sort([7]) == [7]  # => a single element sorts trivially
    assert radix_sort([5, 5, 5]) == [5, 5, 5]  # => all-equal input stays unchanged


# => Run: pytest -- Output: 2 passed
