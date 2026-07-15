"""Capstone step 3a: instrumenting profile (cProfile) of the report pipeline --
identify the hot spot from real tottime, not a guess."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import cProfile  # => co-13: the SAME instrumenting profiler used throughout this whole topic
import pstats  # => co-13: turns cProfile's raw stats into a readable, sorted table
import sys  # => needed only for sys.path.insert below
from io import (
    StringIO,
)  # => co-13: captures pstats' printed table into a string for the print() below

sys.path.insert(
    0, "."
)  # => makes local make_large_batch.py/pipeline.py importable regardless of caller's cwd
from make_large_batch import make_large_batch  # noqa: E402  # => co-13: the SAME large batch step 3b's sampling profile also uses
from pipeline import build_customer_report  # noqa: E402  # => co-13: the FIXED (correctness-wise) pipeline, still O(n^2) on dedupe


def main() -> (
    None
):  # => co-13/co-12: profiles the report pipeline and names the hottest function by tottime
    orders = make_large_batch()  # => co-13: 60,000 orders -- large enough that the O(n^2) dedupe genuinely dominates
    profiler = cProfile.Profile()  # => co-13: a fresh Profile() instance, not the module-level cProfile.run() shortcut
    profiler.enable()  # => co-13: starts intercepting every call/return event from this point on
    build_customer_report(
        orders
    )  # => co-13: the ENTIRE pipeline this profile measures, correctness bug already fixed
    profiler.disable()  # => co-13: stops intercepting -- exact per-call counts are now frozen

    buf = (
        StringIO()
    )  # => co-13: captures pstats' own printed table for a clean, single print() below
    stats = pstats.Stats(profiler, stream=buf).sort_stats(
        pstats.SortKey.TIME
    )  # => co-13: sorted by tottime (self time)
    stats.print_stats(
        5
    )  # => co-13: the top 5 entries -- enough to show dedupe_customers clearly at the top
    print(buf.getvalue())  # => co-13: prints the captured table for a human reader

    top_by_tottime = max(stats.stats.items(), key=lambda kv: kv[1][2])  # type: ignore[attr-defined]  # => co-13: kv[1][2] is tottime
    (_fn, _ln, funcname), _entry = (
        top_by_tottime  # => co-13: unpacks the (file, line, funcname) key -- only funcname matters here
    )
    print(
        f"instrumenting profile's hottest function (by tottime): {funcname!r}"
    )  # => co-13: names the instrumenting profile's answer
    assert funcname == "dedupe_customers", (
        f"expected dedupe_customers to be the hot spot, got {funcname!r}"
    )  # => co-13: the real check


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that profiles and identifies the hot spot
