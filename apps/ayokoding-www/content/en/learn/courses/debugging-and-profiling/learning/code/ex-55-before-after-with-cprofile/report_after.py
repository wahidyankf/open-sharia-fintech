"""Example 55: AFTER -- the fix -- sort ONCE up front instead of every iteration."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fix itself


def build_report(
    rows: list[tuple[str, int]],
) -> list[str]:  # => co-23: the SAME signature as report_before.py
    # co-23: sort once (O(n log n) total) instead of re-sorting on every pop.
    ordered = sorted(
        rows, key=lambda r: r[1]
    )  # => co-23: ONE sort call replaces report_before.py's entire while-loop
    return [
        f"{name}: {value}" for name, value in ordered
    ]  # => co-23: the SAME output shape, built the FAST way
