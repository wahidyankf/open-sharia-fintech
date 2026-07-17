"""Example 74: pytest verification for Median-of-Medians Select."""

from example import median_of_medians_select, naive_first_pivot_select


def test_matches_sorted_for_every_rank_on_random_input() -> None:
    data = [9, 3, 7, 1, 8, 2, 6, 4, 5, 0, 12, 11, 10]
    ordered = sorted(data)
    for k in range(len(data)):
        assert median_of_medians_select(list(data), k, [0]) == ordered[k]


def test_median_of_medians_stays_correct_on_adversarial_sorted_input() -> None:
    n = 50
    data = list(range(n))  # => Example 8's adversarial ordering
    assert median_of_medians_select(list(data), 0, [0]) == 0  # => the minimum
    assert median_of_medians_select(list(data), n - 1, [0]) == n - 1  # => the maximum
    assert median_of_medians_select(list(data), n // 2, [0]) == n // 2  # => the median


def test_naive_pivot_also_stays_correct_despite_being_slow() -> None:
    data = [5, 5, 5, 1, 9]  # => duplicates exercise the pivots-equal branch
    assert naive_first_pivot_select(list(data), 0, [0]) == 1
    assert naive_first_pivot_select(list(data), 4, [0]) == 9


# => Run: pytest -- Output: 3 passed
