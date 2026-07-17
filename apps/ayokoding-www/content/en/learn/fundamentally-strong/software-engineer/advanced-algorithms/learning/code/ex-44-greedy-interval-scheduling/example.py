"""Example 44: Max Non-Overlapping Intervals via Earliest-Finish-Time Greedy."""

# The greedy-choice property (co-22) holds here: always pick the interval
# that FINISHES earliest among the remaining candidates. It never overlaps a
# later-finishing choice's own start, and it leaves maximum room for the rest
# -- a proof-backed optimal strategy, unlike Example 45's failing greedy.


def max_non_overlapping_intervals(
    intervals: list[tuple[int, int]],
) -> list[tuple[int, int]]:  # => (start, end) pairs; returns the chosen subset
    by_finish = sorted(
        intervals, key=lambda iv: iv[1]
    )  # => O(n log n): earliest-finish first
    chosen: list[tuple[int, int]] = []  # => the greedily selected, non-overlapping set
    last_finish = float("-inf")  # => nothing chosen yet -- any interval can start
    for start, end in by_finish:  # => O(n): one pass through finish-sorted intervals
        if start >= last_finish:  # => this interval starts AFTER the last chosen ended
            chosen.append((start, end))  # => safe to take -- no overlap with `chosen`
            last_finish = end  # => this interval's end is now the new cutoff
    return chosen  # => the maximum-count set of mutually non-overlapping intervals


intervals: list[tuple[int, int]] = [
    (1, 4),
    (3, 5),
    (0, 6),
    (5, 7),
    (3, 8),
    (5, 9),
    (6, 10),
    (8, 11),
    (8, 12),
    (2, 13),
    (12, 14),
]  # => the classic CLRS activity-selection example set
chosen = max_non_overlapping_intervals(intervals)  # => the greedy-optimal selection
print(chosen)  # => Output: [(1, 4), (5, 7), (8, 11), (12, 14)]
print(len(chosen))  # => Output: 4

assert len(chosen) == 4  # => confirms the maximum possible count for this instance
for i in range(1, len(chosen)):  # => confirms no two chosen intervals overlap
    assert chosen[i][0] >= chosen[i - 1][1]  # => next start is at/after previous finish
print("ex-44 OK")  # => Output: ex-44 OK
