"""Worked Example 31: Event Time vs. Processing Time."""  # => co-15: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-15: models one event carrying BOTH its own event time and its arrival (processing) time

WINDOW_SIZE_SECONDS = 10  # => co-15: the same fixed window size, now assigned by TWO different clocks


@dataclass  # => co-15: a record's event_time is WHEN IT HAPPENED; arrival_time is WHEN THE PIPELINE SAW IT -- often different
class Event:  # => co-15: one event, carrying two independent timestamps
    event_time_seconds: int  # => co-15: when this event actually occurred, upstream
    arrival_time_seconds: int  # => co-15: when this pipeline actually received it -- can lag event_time_seconds


def window_for(timestamp_seconds: int) -> tuple[int, int]:  # => co-15: the SAME tumbling-window math ex-28 used, reused for either clock
    """Return the fixed tumbling window a timestamp falls into, regardless of which clock produced it."""  # => co-15: documents window_for's contract -- no runtime output, just sets its __doc__
    window_start = (timestamp_seconds // WINDOW_SIZE_SECONDS) * WINDOW_SIZE_SECONDS  # => co-15: floor to the window boundary
    return window_start, window_start + WINDOW_SIZE_SECONDS  # => co-15: returns this computed value to the caller


if __name__ == "__main__":  # => co-15: entry point -- runs only when this file executes directly, not on import
    late_event = Event(event_time_seconds=8, arrival_time_seconds=25)  # => co-15: HAPPENED at t=8s, but only ARRIVED at t=25s -- a LATE event
    event_time_window = window_for(late_event.event_time_seconds)  # => co-15: windowed by WHEN IT HAPPENED
    arrival_time_window = window_for(late_event.arrival_time_seconds)  # => co-15: windowed by WHEN THE PIPELINE SAW IT
    print(f"Event happened at t={late_event.event_time_seconds}s -> event-time window {event_time_window}")  # => co-15
    print(f"Event arrived at t={late_event.arrival_time_seconds}s -> processing-time (arrival) window {arrival_time_window}")  # => co-15

    windows_disagree = event_time_window != arrival_time_window  # => co-15: the claim -- windowing by the two clocks gives DIFFERENT results
    print(f"The two windowing choices disagree: {windows_disagree}")  # => co-15: prints the disagreement check
    assert windows_disagree, "a late event's event-time window must differ from its arrival (processing-time) window"  # => co-15: the claim
    assert event_time_window == (0, 10), "event-time windowing must place this event where it ACTUALLY happened, at t=8s"  # => co-15
    print(f"MATCH: event-time windowing correctly places the event in {event_time_window}, not its arrival window {arrival_time_window}")  # => co-15
    # => co-15: event-time windowing answers "when did this happen"; processing-time windowing only answers "when did we notice it"
