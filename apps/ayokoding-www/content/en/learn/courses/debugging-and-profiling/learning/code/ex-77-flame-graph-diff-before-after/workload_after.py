"""Example 77: AFTER -- the fix -- validate_batch is now O(n), other_stable_work
is UNCHANGED (a real regression check: nothing else should have grown)."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fix itself


def validate_row(
    row: dict[str, str], seen_ids: set[str]
) -> bool:  # => co-19: SAME NAME as workload_before.py -- only the arg type changed
    return (
        row["id"] not in seen_ids
    )  # => co-19/co-23: O(1) set-membership check -- the actual fix over the list version


def validate_batch(
    rows: list[dict[str, str]],
) -> list[bool]:  # => co-19: the SAME caller shape, now genuinely O(n) overall
    seen_ids = {
        row["id"] for row in rows
    }  # => co-19: a SET, not a list -- membership checks against it are O(1) each
    return [
        validate_row(row, seen_ids) for row in rows
    ]  # => co-19: O(n) overall -- n rows, each an O(1) set lookup


def other_stable_work(
    rows: list[dict[str, str]],
) -> int:  # => co-23: IDENTICAL body to workload_before.py's own version
    return sum(
        len(row) for row in rows
    )  # => co-23: unchanged -- confirms the fix touched ONLY validate_row/validate_batch


def pipeline(
    rows: list[dict[str, str]],
) -> None:  # => co-19/co-23: the SAME entry point shape as workload_before.py
    validate_batch(
        rows
    )  # => co-19: now O(n) -- should shrink to a much smaller share of the total profiled time
    other_stable_work(
        rows
    )  # => co-23: unchanged cost -- the regression-check property this example verifies
