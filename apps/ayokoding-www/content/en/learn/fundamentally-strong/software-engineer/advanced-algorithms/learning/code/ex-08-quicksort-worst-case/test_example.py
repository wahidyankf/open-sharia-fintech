"""Example 8: pytest verification for Naive Quicksort's Sorted-Input Blow-Up."""

import example


def test_sorted_input_triggers_exact_worst_case_comparison_count() -> None:
    example.comparisons = 0  # => reset the shared counter before this test's own run
    data: list[int] = list(range(50))  # => a fresh, already-sorted 50-element input
    example.naive_quicksort(data)
    assert example.comparisons == 50 * 49 // 2  # => matches the O(n^2) formula exactly


def test_random_input_uses_far_fewer_comparisons_than_worst_case() -> None:
    import random

    random.seed(1)
    example.comparisons = 0  # => reset before measuring the randomized case
    data: list[int] = random.sample(range(1000), 50)  # => shuffled, not sorted
    example.naive_quicksort(data)
    worst_case = 50 * 49 // 2  # => 1225, the sorted-input worst case
    assert example.comparisons < worst_case  # => random order avoids the O(n^2) trap


# => Run: pytest -- Output: 2 passed
