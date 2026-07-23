"""Example 73: profile the recursion, and show that fixing the WRAPPER (which
has the huge cumtime) does nothing -- the fix has to target expensive_leaf,
found by sorting on tottime, not cumtime.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import cProfile  # => co-13: the SAME instrumenting profiler used throughout this whole topic
import pstats  # => co-13: turns cProfile's raw stats into per-function tottime/cumtime numbers
import sys  # => needed only for sys.path.insert below
from io import (
    StringIO,
)  # => unused output-capture import, kept for parity with this tier's other profiling scripts

sys.path.insert(
    0, "."
)  # => makes local recursive_workload.py importable regardless of caller's cwd
from recursive_workload import recursive_wrapper  # noqa: E402  # => co-16: the SAME recursion this script profiles


def main() -> (
    None
):  # => co-16/co-13: profiles the recursion, then reads BOTH cumtime and tottime for each function
    profiler = cProfile.Profile()  # => co-13: a fresh Profile() instance, not the module-level cProfile.run() shortcut
    profiler.enable()  # => co-13: starts intercepting every call/return event from this point on
    recursive_wrapper(
        depth=50, work_size=20_000
    )  # => co-16: 50 levels of recursion, each calling expensive_leaf once
    profiler.disable()  # => co-13: stops intercepting -- exact per-call counts are now frozen

    stats = pstats.Stats(
        profiler
    )  # => co-13: wraps the raw profile in pstats' queryable form
    wrapper_cumtime = 0.0  # => co-16: recursive_wrapper's OWN cumulative time -- includes every nested call
    wrapper_tottime = (
        0.0  # => co-16: recursive_wrapper's OWN self time -- excludes every nested call
    )
    leaf_tottime = 0.0  # => co-16: expensive_leaf's OWN self time -- the number that actually matters here
    for (_filename, _lineno, funcname), entry in stats.stats.items():  # type: ignore[attr-defined]  # => co-13: one entry per function
        if (
            funcname == "recursive_wrapper"
        ):  # => co-16: filters for the WRAPPER's own stats
            wrapper_cumtime = entry[
                3
            ]  # => co-16: entry[3] is cumtime -- includes the ENTIRE recursive subtree
            wrapper_tottime = entry[
                2
            ]  # => co-16: entry[2] is tottime -- excludes every callee, tiny for a wrapper
        elif funcname == "expensive_leaf":  # => co-16: filters for the LEAF's own stats
            leaf_tottime = entry[
                2
            ]  # => co-16: expensive_leaf's own tottime -- where the real work actually happens

    print(
        f"recursive_wrapper: cumtime={wrapper_cumtime:.4f}s (looks alarming!) tottime={wrapper_tottime:.6f}s (tiny)"
    )  # => co-16
    print(
        f"expensive_leaf:    tottime={leaf_tottime:.4f}s (this is where the time ACTUALLY goes)"
    )  # => co-16: the real answer

    # co-16/co-13: the trap -- a naive read of "which function has the biggest
    # number" (cumtime) points at recursive_wrapper, which is nearly a no-op
    # itself. Sorting by tottime correctly identifies expensive_leaf instead.
    assert wrapper_cumtime > leaf_tottime, (
        "expected the wrapper's cumtime to look bigger than the leaf's tottime"
    )  # => co-16
    assert wrapper_tottime < leaf_tottime / 10, (
        "expected the wrapper's OWN tottime to be tiny compared to the leaf's"
    )  # => co-16
    print(
        "confirmed: the wrapper's cumtime is a trap -- tottime correctly points at expensive_leaf as the real hot spot"
    )  # => co-16


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that profiles, compares, and reports the trap
