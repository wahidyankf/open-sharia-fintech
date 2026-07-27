"""Worked Example 32: Watermark Progress -- Windows Emit Only Once the Watermark Passes."""  # => co-15: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

WINDOW_END_SECONDS = 10  # => co-15: the window under watch -- [0, 10)


def window_has_emitted(watermark_seconds: int) -> bool:  # => co-15: a window emits once the watermark has passed its END
    """A window emits its result once the watermark has advanced past the window's own end."""  # => co-15: documents window_has_emitted's contract -- no runtime output, just sets its __doc__
    return watermark_seconds >= WINDOW_END_SECONDS  # => co-15: the watermark, not the wall clock, decides when a window is "done"


if __name__ == "__main__":  # => co-15: entry point -- runs only when this file executes directly, not on import
    watermark_progress_seconds = [3, 6, 9, 10, 11]  # => co-15: the watermark's own progress over time -- monotonically advancing
    emission_status: dict[int, bool] = {}  # => co-15: for each watermark value, has WINDOW_END_SECONDS's window emitted yet?
    for watermark in watermark_progress_seconds:  # => co-15: check the window's emission status at each watermark checkpoint
        emission_status[watermark] = window_has_emitted(watermark)  # => co-15: record whether the window has emitted at this point
        print(f"  watermark={watermark}s -> window [0,{WINDOW_END_SECONDS}) has emitted: {emission_status[watermark]}")  # => co-15

    emits_only_after_pass = (  # => co-15: the claim -- emission stays False right up until the watermark reaches the window's end
        emission_status[9] is False and emission_status[10] is True  # => co-15: the two boundary watermark values -- one tick before the window ends, and exactly at it
    )  # => co-15: watermark=9 (before window end) must NOT have emitted; watermark=10 (at window end) MUST have emitted
    print(f"Window emits only once watermark reaches its end (not before): {emits_only_after_pass}")  # => co-15
    assert emits_only_after_pass, "a window must emit only once the watermark passes its end, never earlier"  # => co-15: the claim ex-32 makes
    print(f"MATCH: window [0,{WINDOW_END_SECONDS}) stayed silent through watermark=9s, then emitted at watermark=10s")  # => co-15
    # => co-15: the watermark is the engine's own promise about how much event-time progress has been made -- windows trust it, not the wall clock
