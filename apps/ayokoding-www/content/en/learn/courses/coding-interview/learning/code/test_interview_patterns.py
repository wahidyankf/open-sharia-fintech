"""Executable checks for original Coding Interview reference routines."""

from interview_patterns import (
    first_last,
    longest_unique,
    min_coin_count,
    min_cover,
    next_greater,
    schedule,
    shortest_grid_path,
    top_k,
    two_sum_indices,
)


def test_two_sum_returns_distinct_indices_and_handles_absence() -> None:
    assert two_sum_indices([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum_indices([3], 6) is None


def test_window_and_binary_search_boundaries() -> None:
    assert longest_unique("abba") == 2
    assert first_last([1, 2, 2, 2, 3], 2) == (1, 3)
    assert first_last([], 2) == (-1, -1)


def test_bfs_and_dynamic_programming_edge_cases() -> None:
    assert shortest_grid_path([[0, 0], [1, 0]]) == 2
    assert shortest_grid_path([[1]]) == -1
    assert min_coin_count([1, 3, 4], 6) == 2
    assert min_coin_count([2], 3) == -1


def test_greedy_heap_and_monotonic_stack() -> None:
    assert schedule([(0, 6), (1, 2), (3, 4), (5, 7)]) == [(1, 2), (3, 4), (5, 7)]
    assert top_k([4, 1, 8, 2, 9, 3], 3) == [9, 8, 4]
    assert next_greater([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]


def test_minimum_cover_preserves_required_multiplicity() -> None:
    assert min_cover("ADOBECODEBANC", "ABC") == "BANC"
    assert min_cover("a", "aa") == ""
