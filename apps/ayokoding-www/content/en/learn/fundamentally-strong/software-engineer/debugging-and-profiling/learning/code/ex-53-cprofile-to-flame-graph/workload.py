"""Example 53: a workload with one clear hot function, profiled two independent ways."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself


def slow_transform(
    rows: list[int],
) -> list[int]:  # => co-13: the function BOTH profilers should agree is hot
    # co-13: the deliberate hot spot -- an O(n) pass with an expensive-ish inner op.
    return [
        sum(str(r * 37 + i).__len__() for i in range(30)) for r in rows
    ]  # => co-13: the <genexpr> lives HERE


def cheap_filter(
    rows: list[int],
) -> list[int]:  # => co-13: a DELIBERATELY cheap function -- the negative control
    return [
        r for r in rows if r % 2 == 0
    ]  # => co-13: O(n), no inner loop -- should show up as cold in both profiles


def pipeline(
    rows: list[int],
) -> list[int]:  # => co-13: the entry point both make_prof.py and the sampler call
    filtered = cheap_filter(
        rows
    )  # => co-13: runs first, contributes almost nothing to either profile's total
    return slow_transform(
        filtered
    )  # => co-13: runs second -- where nearly all of pipeline()'s own time goes
