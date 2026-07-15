"""Example 53: generate a real .prof file via cProfile."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import cProfile  # => co-13: the SAME instrumenting profiler used throughout this whole topic
import sys  # => needed only for sys.path.insert below -- workload.py lives next to this script, not on sys.path

sys.path.insert(
    0, "."
)  # => co-13: makes the local workload.py importable regardless of the caller's cwd
from workload import pipeline  # noqa: E402  # => co-13: the SAME pipeline() gprof2dot and mini_sampler will also see


def main() -> (
    None
):  # => co-13: writes workload.prof, the ONE artifact this whole example is built around
    rows = list(
        range(20_000)
    )  # => co-13: large enough that slow_transform()'s inner genexpr genuinely dominates
    profiler = cProfile.Profile()  # => co-13: a fresh Profile() instance, not the module-level cProfile.run() shortcut
    profiler.enable()  # => co-13: starts intercepting every call/return event from this point on
    pipeline(rows)  # => co-13: the ENTIRE workload this .prof file will describe
    profiler.disable()  # => co-13: stops intercepting -- exact per-call counts are now frozen
    profiler.dump_stats(
        "workload.prof"
    )  # => co-13: the binary pstats file gprof2dot reads in the next step
    print(
        "wrote workload.prof"
    )  # => confirms the file exists before the next command tries to read it


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that produces workload.prof
