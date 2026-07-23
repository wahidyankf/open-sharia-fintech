"""Example 55: profile BEFORE and AFTER with cProfile, and measure the tottime
share of `build_report` dropping -- the concrete, quantified "did it help?" check.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import cProfile  # => co-13: the SAME instrumenting profiler used throughout this whole topic
import importlib  # => co-13: loads report_before/report_after by NAME, so one function covers both
import pstats  # => co-13: turns cProfile's raw stats into per-function tottime/cumtime numbers
import sys  # => needed only for sys.path.insert below
from io import (
    StringIO,
)  # => swallows pstats' own printed table -- this script reports its own summary instead

sys.path.insert(
    0, "."
)  # => makes local report_before.py/report_after.py importable regardless of caller's cwd


def profile_module(
    module_name: str, rows: list[tuple[str, int]]
) -> tuple[float, float]:  # => co-23/co-13: one profiling run
    module = importlib.import_module(
        module_name
    )  # => co-13: dynamically loads "report_before" or "report_after"
    profiler = cProfile.Profile()  # => co-13: a fresh Profile() instance per call -- BEFORE and AFTER never share state
    profiler.enable()  # => co-13: starts intercepting every call/return event
    module.build_report(
        rows
    )  # => co-13: the SAME rows, run through whichever module was requested
    profiler.disable()  # => co-13: stops intercepting -- exact per-call counts are now frozen
    stats = pstats.Stats(
        profiler
    )  # => co-13: wraps the raw profile in pstats' queryable form
    total_tt = sum(entry[2] for entry in stats.stats.values())  # type: ignore[attr-defined]  # => co-13: sums EVERY function's own tottime
    build_report_tt = 0.0  # => co-23: tracks build_report's OWN tottime specifically, not the whole run
    for (_filename, _lineno, funcname), entry in stats.stats.items():  # type: ignore[attr-defined]  # => co-13: one entry per profiled function
        if (
            funcname == "build_report"
        ):  # => co-23: filters for the ONE function this example is measuring
            build_report_tt = entry[
                2
            ]  # => co-23: entry[2] is tottime -- this function's OWN time, not its callees'
    return (
        build_report_tt,
        total_tt,
    )  # => co-23/co-13: both numbers the caller needs for a percentage


def main() -> (
    None
):  # => co-23: runs BEFORE then AFTER, and asserts the fix is a measurable improvement
    rows = [
        (f"item-{i}", (i * 37) % 5000) for i in range(1500)
    ]  # => co-23: the SAME 1,500-row input for BOTH profiles

    before_tt, before_total = profile_module(
        "report_before", rows
    )  # => co-23: the SLOW, O(n^2) implementation
    before_pct = (
        before_tt / before_total * 100
    )  # => co-23: build_report's OWN share of the total wall time
    print(
        f"BEFORE: build_report tottime={before_tt:.4f}s of {before_total:.4f}s total ({before_pct:.1f}%)"
    )  # => co-23

    after_tt, after_total = profile_module(
        "report_after", rows
    )  # => co-23: the FAST, sorted() implementation
    after_pct = (
        after_tt / after_total * 100
    )  # => co-23: the SAME share, computed the SAME way, for comparison
    print(
        f"AFTER:  build_report tottime={after_tt:.4f}s of {after_total:.4f}s total ({after_pct:.1f}%)"
    )  # => co-23

    assert after_total < before_total, (
        "expected the AFTER version to be measurably faster overall"
    )  # => co-23
    drop = (
        before_total - after_total
    )  # => co-23: the raw wall-time improvement, in seconds
    drop_pct = (
        drop / before_total * 100
    )  # => co-23: the SAME improvement, as a percentage of the BEFORE total
    print(
        f"total wall time dropped by {drop:.4f}s ({drop_pct:.1f}%) after the fix"
    )  # => co-23: the headline number
    assert drop_pct > 50, (
        f"expected at least a 50% total-time drop, got {drop_pct:.1f}%"
    )  # => co-23: a real floor, not a token one

    # co-23/co-13: the hot spot's OWN tottime share (not just overall wall time)
    # must also have dropped -- that is the specific "did the fix target the
    # right leaf function" check, not just "did the program get faster overall".
    print(
        f"build_report's tottime share: BEFORE {before_pct:.1f}% -> AFTER {after_pct:.1f}%"
    )  # => co-23/co-13
    assert after_pct < before_pct, (
        "expected build_report's own tottime SHARE to drop after the fix"
    )  # => co-23/co-13
    print(
        "confirmed: the fix produced a measurable, quantified improvement in both total time and tottime share"
    )  # => co-23


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that profiles BEFORE, profiles AFTER, and reports the measured delta
