"""Example 10: pytest verification for In-Place Heapsort."""

import random

from example import heapsort


def test_matches_builtin_sorted_on_random_input() -> None:
    random.seed(5)
    data: list[int] = random.sample(range(1000), 60)
    expected = sorted(data)
    heapsort(data)
    assert data == expected  # => heapsort's in-place result matches sorted()


def test_reverse_sorted_input_is_the_classic_stress_case() -> None:
    data: list[int] = list(range(30, 0, -1))  # => strictly descending -- worst-ish case
    heapsort(data)
    assert data == list(range(1, 31))  # => ends up strictly ascending


# => Run: pytest -- Output: 2 passed
