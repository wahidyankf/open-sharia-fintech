"""Worked Example 28: Tumbling Window -- Fixed, Non-Overlapping."""  # => co-14: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

WINDOW_SIZE_SECONDS = 10  # => co-14: every tumbling window is exactly this wide, back to back, never overlapping


def tumbling_window_for(event_time_seconds: int) -> tuple[int, int]:  # => co-14: maps ONE event to its ONE tumbling window
    """Return the (start, end) of the fixed, non-overlapping window an event at this time falls into."""  # => co-14: documents tumbling_window_for's contract -- no runtime output, just sets its __doc__
    window_start = (event_time_seconds // WINDOW_SIZE_SECONDS) * WINDOW_SIZE_SECONDS  # => co-14: floor to the nearest window boundary
    return window_start, window_start + WINDOW_SIZE_SECONDS  # => co-14: returns this computed value to the caller -- [start, end)


if __name__ == "__main__":  # => co-14: entry point -- runs only when this file executes directly, not on import
    events = [2, 9, 10, 15, 23, 29, 30]  # => co-14: seven event timestamps, in seconds, spanning four tumbling windows
    assignments = {event: tumbling_window_for(event) for event in events}  # => co-14: one window assignment PER event
    for event, window in assignments.items():  # => co-14: one line per event, showing which window it landed in
        print(f"  event at t={event}s -> window {window}")  # => co-14: prints the (start, end) window each event fell into

    distinct_windows = sorted(set(assignments.values()))  # => co-14: how many DISTINCT windows were actually touched
    print(f"Distinct windows touched: {distinct_windows}")  # => co-14: prints the window boundaries -- [0,10), [10,20), [20,30), [30,40)
    windows_are_adjacent = all(  # => co-14: consecutive windows must share a boundary with NO gap and NO overlap
        distinct_windows[i][1] == distinct_windows[i + 1][0]
        for i in range(len(distinct_windows) - 1)  # => co-14: compares every adjacent pair of the four distinct windows
    )  # => co-14: each window's end EXACTLY equals the next window's start
    each_event_in_exactly_one_window = len(assignments) == len(events)  # => co-14: a dict comprehension already guarantees this, made explicit
    print(f"Windows adjacent, no gaps or overlaps: {windows_are_adjacent} | Every event in exactly one window: {each_event_in_exactly_one_window}")  # => co-14
    assert windows_are_adjacent, "tumbling windows must be fixed-size and non-overlapping, back to back"  # => co-14: the claim
    assert each_event_in_exactly_one_window, "every event must fall into exactly one tumbling window"  # => co-14
    print(f"MATCH: {len(events)} events, {len(distinct_windows)} distinct non-overlapping tumbling windows")  # => co-14
    # => co-14: tumbling windows are the simplest stream-window shape -- every second belongs to exactly one window, forever
