"""Example 77: BEFORE -- a slow, O(n^2) validate_batch, dominating the profile."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the hot spot itself


def validate_row(
    row: dict[str, str], all_ids: list[str]
) -> bool:  # => co-19: the LEAF whose name stays the SAME after the fix
    return (
        row["id"] not in all_ids
    )  # => co-19: O(n) list-membership check, called per row -- the hot spot's own cost


def validate_batch(
    rows: list[dict[str, str]],
) -> list[bool]:  # => co-19: the caller -- O(n) rows times O(n) membership = O(n^2)
    all_ids = [
        row["id"] for row in rows
    ]  # => co-19: a plain LIST -- membership checks against it are O(n) each
    return [
        validate_row(row, all_ids) for row in rows
    ]  # => co-19: O(n^2) overall -- n rows, each an O(n) list scan


def other_stable_work(
    rows: list[dict[str, str]],
) -> int:  # => co-23: the REGRESSION CHECK function -- should NOT change cost
    return sum(
        len(row) for row in rows
    )  # => co-23: cheap, O(n) work that stays constant across BEFORE and AFTER


def pipeline(
    rows: list[dict[str, str]],
) -> None:  # => co-19/co-23: the entry point BOTH cProfile and mini_sampler profile
    validate_batch(
        rows
    )  # => co-19: the O(n^2) hot spot -- dominates this pipeline's total time BEFORE the fix
    other_stable_work(
        rows
    )  # => co-23: unrelated work -- its cost should be IDENTICAL in workload_after.py
