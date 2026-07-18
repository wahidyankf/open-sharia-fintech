"""Example 27: pytest verification for Randomized-Pivot Quicksort."""

import random

import example


def test_sorted_input_no_longer_hits_the_naive_worst_case() -> None:
    random.seed(3)
    n = 300
    data: list[int] = list(range(n))
    example.comparisons = 0
    example.randomized_quicksort(data)
    naive_worst_case = n * (n - 1) // 2
    assert example.comparisons < naive_worst_case  # => far below the O(n^2) bound
    assert data == list(range(n))  # => still correctly sorted


def test_matches_sorted_on_random_input() -> None:
    random.seed(4)
    data: list[int] = random.sample(range(1000), 60)
    expected = sorted(data)
    example.randomized_quicksort(data)
    assert data == expected


# => Run: pytest -- Output: 2 passed
