"""Example 44: pytest verification for Greedy Interval Scheduling."""

from example import max_non_overlapping_intervals


def test_no_two_chosen_intervals_overlap() -> None:
    intervals = [(1, 3), (2, 4), (3, 5), (0, 6), (5, 7)]
    chosen = max_non_overlapping_intervals(intervals)
    for i in range(1, len(chosen)):
        assert chosen[i][0] >= chosen[i - 1][1]


def test_matches_the_known_optimal_count() -> None:
    intervals = [(1, 2), (2, 3), (3, 4), (1, 4)]  # => three tiny + one that blocks all
    chosen = max_non_overlapping_intervals(intervals)
    assert len(chosen) == 3  # => (1,2), (2,3), (3,4) -- the big one loses out


# => Run: pytest -- Output: 2 passed
