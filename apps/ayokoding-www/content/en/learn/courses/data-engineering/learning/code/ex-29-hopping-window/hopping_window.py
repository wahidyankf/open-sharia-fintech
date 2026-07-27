"""Worked Example 29: Hopping Window -- Overlapping, Advance Less Than Size."""  # => co-14: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

WINDOW_SIZE_SECONDS = 10  # => co-14: each hopping window is 10 seconds wide -- WIDER than the advance below
HOP_SIZE_SECONDS = 5  # => co-14: windows advance by only 5 seconds -- LESS than the window size, so windows overlap


def hopping_windows_for(event_time_seconds: int) -> list[tuple[int, int]]:  # => co-14: an event can fall into MULTIPLE hopping windows
    """Return every (start, end) hopping window this event's timestamp falls inside."""  # => co-14: documents hopping_windows_for's contract -- no runtime output, just sets its __doc__
    matches: list[tuple[int, int]] = []  # => co-14: accumulates every window that contains this event
    for candidate_start in range(0, event_time_seconds + 1, HOP_SIZE_SECONDS):  # => co-14: every window start is a multiple of the HOP size, from 0
        window = (candidate_start, candidate_start + WINDOW_SIZE_SECONDS)  # => co-14: this window's (start, end)
        if window[0] <= event_time_seconds < window[1]:  # => co-14: confirm the event actually falls INSIDE this window
            matches.append(window)  # => co-14: this window genuinely contains the event
    return matches  # => co-14: returns this computed value to the caller


if __name__ == "__main__":  # => co-14: entry point -- runs only when this file executes directly, not on import
    event_time = 12  # => co-14: ONE event, at t=12 seconds
    matched_windows = hopping_windows_for(event_time)  # => co-14: every hopping window this single event belongs to
    print(f"Event at t={event_time}s falls into windows: {sorted(matched_windows)}")  # => co-14: prints all matching windows

    appears_in_multiple_windows = len(matched_windows) > 1  # => co-14: the defining property of hopping (vs. tumbling) windows
    print(f"Event appears in more than one window: {appears_in_multiple_windows}")  # => co-14: prints the multiplicity check
    assert appears_in_multiple_windows, "a hopping window's overlap must place at least one event in more than one window"  # => co-14
    assert set(matched_windows) == {(5, 15), (10, 20)}, "t=12 must fall inside exactly windows [5,15) and [10,20)"  # => co-14: the exact expected set
    print(f"MATCH: t={event_time}s appears in {len(matched_windows)} overlapping windows -- {sorted(matched_windows)}")  # => co-14
    # => co-14: hopping (Kafka Streams calls this "sliding") is tumbling with an advance SMALLER than the window -- overlap by design
