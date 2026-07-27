"""Worked Example 30: Session Window -- Group by Inactivity Gap."""  # => co-14: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

SESSION_GAP_SECONDS = 30  # => co-14: a session ends once this many seconds pass with NO activity -- unlike tumbling/hopping, size is data-driven


def build_sessions(event_times: list[int]) -> list[list[int]]:  # => co-14: groups events into sessions based on ACTIVITY, not a fixed clock
    """Group sorted event timestamps into sessions, starting a new one after any gap >= SESSION_GAP_SECONDS."""  # => co-14: documents build_sessions's contract -- no runtime output, just sets its __doc__
    sessions: list[list[int]] = []  # => co-14: accumulates one list of event times PER session
    for event_time in sorted(event_times):  # => co-14: process events in time order -- session boundaries depend on GAPS between them
        if sessions and event_time - sessions[-1][-1] < SESSION_GAP_SECONDS:  # => co-14: still within the gap of the LAST event -- same session
            sessions[-1].append(event_time)  # => co-14: extend the current, still-active session
        else:  # => co-14: either the very first event, or the gap since the last event exceeded the threshold
            sessions.append([event_time])  # => co-14: START a brand-new session
    return sessions  # => co-14: returns this computed value to the caller


if __name__ == "__main__":  # => co-14: entry point -- runs only when this file executes directly, not on import
    events = [0, 5, 12, 50, 55, 100]  # => co-14: a burst, then a 38s gap, then another burst, then a 45s gap, then one lone event
    sessions = build_sessions(events)  # => co-14: compute the sessions from the raw event times
    for index, session in enumerate(sessions):  # => co-14: one line per discovered session
        print(f"  session {index}: {session}")  # => co-14: prints each session's member events

    print(f"Number of sessions discovered: {len(sessions)}")  # => co-14: prints the session count
    new_session_started_after_gap = sessions == [[0, 5, 12], [50, 55], [100]]  # => co-14: the EXACT expected session boundaries
    print(f"Matches expected session boundaries: {new_session_started_after_gap}")  # => co-14: prints the boundary check
    assert new_session_started_after_gap, "a new session must start exactly once the inactivity gap elapses"  # => co-14: the claim
    print(f"MATCH: {len(sessions)} sessions, each boundary driven by a {SESSION_GAP_SECONDS}s+ gap in activity, not a fixed clock")  # => co-14
    # => co-14: session windows are the one window type whose SIZE is not fixed at all -- it is entirely a function of the data
