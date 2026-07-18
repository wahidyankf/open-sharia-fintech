"""Example 52: pytest verification for Binary Search Boundaries."""

from example import leftmost_index, rightmost_index


def test_leftmost_and_rightmost_bracket_a_run_of_duplicates() -> None:
    data = [1, 3, 3, 3, 3, 7, 9]
    assert leftmost_index(data, 3) == 1
    assert rightmost_index(data, 3) == 4


def test_absent_target_returns_negative_one_both_ways() -> None:
    data = [2, 4, 6, 8]
    assert leftmost_index(data, 5) == -1
    assert rightmost_index(data, 5) == -1


def test_single_occurrence_matches_on_both_boundaries() -> None:
    data = [10, 20, 30]
    assert leftmost_index(data, 20) == rightmost_index(data, 20) == 1


# => Run: pytest -- Output: 3 passed
