"""Example 44: Max Non-Overlapping Intervals via Earliest-Finish-Time Greedy."""

# The greedy-choice property (co-22) holds here: always pick the interval
# that FINISHES earliest among the remaining candidates. It never overlaps a
# later-finishing choice's own start, and it leaves maximum room for the rest
# -- a proof-backed optimal strategy, unlike Example 45's failing greedy.


def max_non_overlapping_intervals(  # => sort by finish time, then greedily take non-overlapping
    intervals: list[tuple[int, int]],  # => a list of (start, end) candidate intervals
) -> list[tuple[int, int]]:  # => (start, end) pairs; returns the chosen subset
    by_finish = sorted(  # => opens the earliest-finish-first sort
        intervals,
        key=lambda iv: iv[1],  # => sorts by the END field only
    )  # => O(n log n): earliest-finish first
    chosen: list[tuple[int, int]] = []  # => the greedily selected, non-overlapping set
    last_finish = float("-inf")  # => nothing chosen yet -- any interval can start
    for start, end in by_finish:  # => O(n): one pass through finish-sorted intervals
        if start >= last_finish:  # => this interval starts AFTER the last chosen ended
            chosen.append((start, end))  # => safe to take -- no overlap with `chosen`
            last_finish = end  # => this interval's end is now the new cutoff
    return chosen  # => the maximum-count set of mutually non-overlapping intervals


intervals: list[tuple[int, int]] = [  # => opens the classic CLRS activity-selection set
    (1, 4),  # => finishes 3rd-earliest -- a likely early pick
    (3, 5),  # => overlaps (1, 4) -- competes for the same early slot
    (
        0,
        6,
    ),  # => starts earliest but finishes late -- likely skipped in favor of shorter ones
    (5, 7),  # => finishes early enough to chain after (1, 4)
    (3, 8),  # => a long interval overlapping several others
    (5, 9),  # => overlaps (5, 7) -- competes for the same slot
    (6, 10),  # => overlaps (5, 7) -- starts before it finishes
    (8, 11),  # => starts right where (5, 7) ends -- a valid chain candidate
    (8, 12),  # => overlaps (8, 11) -- competes for the same slot
    (2, 13),  # => a very long interval, overlapping nearly everything
    (12, 14),  # => starts right where (8, 11) ends -- another valid chain candidate
]  # => the classic CLRS activity-selection example set
chosen = max_non_overlapping_intervals(intervals)  # => the greedy-optimal selection
print(chosen)  # => Output: [(1, 4), (5, 7), (8, 11), (12, 14)]
print(len(chosen))  # => Output: 4

assert len(chosen) == 4  # => confirms the maximum possible count for this instance
for i in range(1, len(chosen)):  # => confirms no two chosen intervals overlap
    assert chosen[i][0] >= chosen[i - 1][1]  # => next start is at/after previous finish
print("ex-44 OK")  # => Output: ex-44 OK
