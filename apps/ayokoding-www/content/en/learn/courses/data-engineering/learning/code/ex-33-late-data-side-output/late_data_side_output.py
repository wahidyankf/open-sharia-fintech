"""Worked Example 33: Late Data -- Side Output, Not Silent Drop."""  # => co-15: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-15: models routing late events to a captured side output, not /dev/null

WINDOW_END_SECONDS = 10  # => co-15: the window this stream is watching -- [0, 10)
ALLOWED_LATENESS_SECONDS = 5  # => co-15: a grace period -- events up to this late past the window end still count, per Flink/Kafka Streams docs


@dataclass  # => co-15: a router that separates on-time events from late ones, capturing BOTH instead of discarding late ones
class WindowRouter:  # => co-15: models the on-time path plus a captured side output for anything genuinely too late
    on_time: list[int] = field(default_factory=list)  # => co-15: events the window's own allowed-lateness grace period still accepts
    side_output: list[int] = field(default_factory=list)  # => co-15: events that arrived AFTER the grace period -- captured, not dropped

    def route(self, event_time_seconds: int, watermark_seconds: int) -> None:  # => co-15: decide on-time vs. side-output for one event
        """Route an event to on_time if within the grace period of the watermark, else to side_output -- never silently drop it."""  # => co-15: documents route's contract -- no runtime output, just sets its __doc__
        deadline = WINDOW_END_SECONDS + ALLOWED_LATENESS_SECONDS  # => co-15: the true cutoff -- window end PLUS the grace period
        if watermark_seconds <= deadline:  # => co-15: still within the allowed-lateness grace period
            self.on_time.append(event_time_seconds)  # => co-15: accepted into the window's normal result
        else:  # => co-15: past even the grace period -- genuinely too late for this window
            self.side_output.append(event_time_seconds)  # => co-15: CAPTURED here, not thrown away


if __name__ == "__main__":  # => co-15: entry point -- runs only when this file executes directly, not on import
    router = WindowRouter()  # => co-15: a fresh router, nothing routed yet
    router.route(event_time_seconds=4, watermark_seconds=6)  # => co-15: comfortably on time
    router.route(event_time_seconds=9, watermark_seconds=13)  # => co-15: late, but within the 5s grace period (deadline is 15)
    router.route(event_time_seconds=2, watermark_seconds=20)  # => co-15: genuinely late -- watermark 20 exceeds the deadline of 15
    print(f"On-time (including within grace period): {router.on_time}")  # => co-15: prints the accepted events
    print(f"Side output (too late even for the grace period): {router.side_output}")  # => co-15: prints the captured-not-dropped late events

    nothing_silently_dropped = len(router.on_time) + len(router.side_output) == 3  # => co-15: every routed event lands SOMEWHERE
    print(f"Every routed event captured somewhere (nothing dropped): {nothing_silently_dropped}")  # => co-15
    assert nothing_silently_dropped, "late events must be captured in the side output, never silently discarded"  # => co-15: the claim
    assert router.side_output == [2], "only the event past the allowed-lateness deadline belongs in the side output"  # => co-15
    print(f"MATCH: {len(router.on_time)} on-time events, {len(router.side_output)} captured late events, 0 silently dropped")  # => co-15
    # => co-15: a side output is what lets a late-arriving batch still be investigated or reprocessed, instead of vanishing
