"""Tests that make all five coding-round capstone solutions runnable."""

from round import (
    count_islands,
    longest_sum_at_most,
    pair_indices,
    select_meetings,
    streaming_top_k,
)


def test_pair_indices() -> None:
    assert pair_indices([4, 5, 1, 8], 9) == (0, 1)


def test_compact_window() -> None:
    assert longest_sum_at_most([2, 1, 1, 2, 1], 4) == 3


def test_islands() -> None:
    assert count_islands([[0, 1, 0], [0, 1, 1], [1, 0, 0]]) == 3


def test_meeting_selection() -> None:
    assert select_meetings([(0, 6), (1, 2), (3, 5), (5, 7)]) == [(1, 2), (3, 5), (5, 7)]


def test_streaming_top_k() -> None:
    assert streaming_top_k([5, 1, 9, 2, 8], 2) == [9, 8]
