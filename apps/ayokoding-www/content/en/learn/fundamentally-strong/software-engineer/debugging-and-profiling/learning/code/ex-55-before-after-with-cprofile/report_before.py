"""Example 55: BEFORE -- a report builder with a real hot spot -- an O(n^2) pure-Python
linear scan for the next-smallest item, done directly in `build_report`'s own bytecode
(not delegated to a C builtin), so the self time (tottime) is genuinely dominated by
`build_report` itself.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the hot spot itself


def build_report(
    rows: list[tuple[str, int]],
) -> list[str]:  # => co-23: the function BOTH profiles will target
    lines: list[
        str
    ] = []  # => co-23: accumulates the sorted-by-value output, one line per remaining item
    remaining = list(
        rows
    )  # => co-23: a MUTABLE copy -- .pop() below shrinks it, the input list stays untouched
    while remaining:  # => co-23: O(n) outer iterations -- one per item removed
        # co-23: the hot spot -- a hand-rolled O(n) linear scan for the minimum,
        # run once per remaining item (O(n^2) overall), executed entirely as
        # Python bytecode INSIDE this function -- not inside any builtin call.
        min_index = 0  # => co-23: assumes the FIRST remaining item is smallest until proven otherwise
        for i in range(
            1, len(remaining)
        ):  # => co-23: the O(n) INNER scan -- this is what makes it O(n^2) overall
            if (
                remaining[i][1] < remaining[min_index][1]
            ):  # => co-23: compares by the tuple's second field (value)
                min_index = i  # => co-23: updates the running minimum's index
        name, value = remaining.pop(
            min_index
        )  # => co-23: removes the found minimum -- O(n) shift, on top of the scan
        lines.append(
            f"{name}: {value}"
        )  # => co-23: appends in ascending-value order, one item per outer iteration
    return lines  # => co-23: the final sorted-by-value report, built the SLOW way
