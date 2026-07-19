# learning/code/ex-39-iterate-on-feedback/iterate_feedback.py
"""Example 39: Iterating on a Failed First Attempt via Feedback."""  # => co-23: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-23: types the parse_fn parameter acceptance_test is quantified over


def parse_iso_date_v1(date_str: str) -> tuple[int, int, int]:  # => co-23: the agent's FIRST generation, before any feedback
    """First agent attempt: splits on '-' -- works for a plain YYYY-MM-DD date only."""  # => co-23: documents parse_iso_date_v1's contract -- no runtime output, just sets its __doc__
    year, month, day = date_str.split("-")  # => co-23: BUG -- a full timestamp's "day" segment still carries "T09:30:00Z"
    return int(year), int(month), int(day)  # => co-23: int() on a contaminated day segment is exactly where this breaks


def parse_iso_date_v2(date_str: str) -> tuple[int, int, int]:  # => co-23: the SECOND generation, produced after the feedback below
    """Second attempt, after feedback: strips a trailing time/timezone component first."""  # => co-23: documents parse_iso_date_v2's contract -- no runtime output, just sets its __doc__
    date_part = date_str.split("T")[0]  # => co-23: the fix -- drop everything from "T" onward BEFORE splitting on "-"
    year, month, day = date_part.split("-")  # => co-23: now only ever sees a clean YYYY-MM-DD segment
    return int(year), int(month), int(day)  # => co-23: safe -- day is guaranteed to be a plain two-digit string here


def acceptance_test(parse_fn: Callable[[str], tuple[int, int, int]]) -> None:  # => co-23: the FIXED acceptance bar -- unchanged across both attempts
    """The fixed acceptance bar: a plain date AND a full ISO 8601 timestamp must both parse."""  # => co-23: documents acceptance_test's contract -- no runtime output, just sets its __doc__
    assert parse_fn("2026-07-18") == (2026, 7, 18), "must parse a plain date"  # => co-23: case 1 -- both attempts are expected to pass this one
    assert parse_fn("2026-07-18T09:30:00Z") == (2026, 7, 18), "must parse a full ISO 8601 timestamp"  # => co-23: case 2 -- only v2 is expected to pass this one


if __name__ == "__main__":  # => co-23: entry point -- this block runs only when the file executes directly, not on import
    print("--- first attempt ---")  # => co-23: labels the first-generation block of this transcript
    try:  # => co-23: v1 is EXPECTED to fail the timestamp case
        acceptance_test(parse_iso_date_v1)  # => co-23: runs the fixed acceptance bar against the first generation
        first_passed = True  # => co-23: reached only if v1 unexpectedly passed both cases
    except (AssertionError, ValueError) as exc:  # => co-23: either failure mode counts as a genuine first-attempt failure
        first_passed = False  # => co-23: records the genuine failure, not just that code ran
        print(f"FAILED: {exc}")  # => co-23: the captured failure message from the first generation
    print(f"first attempt passed: {first_passed}")  # => co-23: expect False

    feedback = (  # => co-23: the EXACT gap fed back to the agent -- not a vague "try again"
        "The plain-date case passed, but parse_iso_date_v1('2026-07-18T09:30:00Z') raised "  # => co-23: names which case failed
        "a ValueError -- it never strips the time component before splitting on '-'."  # => co-23: names the ROOT CAUSE, not just the symptom
    )  # => co-23: closes the multi-line construct opened above
    print(f"\nfeedback given to the agent: {feedback}")  # => co-23: the feedback text, logged verbatim in this transcript

    print("\n--- second attempt (after feedback) ---")  # => co-23: labels the second-generation block of this transcript
    try:  # => co-23: v2 is EXPECTED to pass both cases, incorporating the feedback above
        acceptance_test(parse_iso_date_v2)  # => co-23: runs the SAME fixed acceptance bar against the second generation
        second_passed = True  # => co-23: reached only if v2 passed both cases
    except (AssertionError, ValueError) as exc:  # => co-23: would indicate the fix was itself wrong
        second_passed = False  # => co-23: records a genuine second-attempt failure, if one occurred
        print(f"FAILED: {exc}")  # => co-23: the captured failure message, if any
    print(f"second attempt passed: {second_passed}")  # => co-23: expect True

    assert not first_passed, "the first attempt must genuinely fail the timestamp case"  # => co-23: proves this was a REAL red, not staged
    assert second_passed, "the second attempt must pass both cases after feedback"  # => co-23: proves the fix genuinely closed the gap
    print("\nSecond diff passes where the first did not: True")  # => co-23: this file is self-verifying -- a clean exit proves the claim held
