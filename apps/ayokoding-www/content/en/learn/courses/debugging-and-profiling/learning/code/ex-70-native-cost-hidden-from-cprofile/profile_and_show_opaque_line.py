"""Example 70: profile hash_many with cProfile, and show that the sha256 cost
collapses to a single opaque line -- no internal breakdown of the C code inside
OpenSSL's sha256 implementation is possible from cProfile alone.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import cProfile  # => co-13: the SAME instrumenting profiler used throughout this whole topic
import pstats  # => co-13: turns cProfile's raw stats into a readable, sorted table
import sys  # => needed only for sys.path.insert below
from io import (
    StringIO,
)  # => co-13: captures pstats' printed table into a string, so this script can inspect it too

sys.path.insert(
    0, "."
)  # => makes local hash_workload.py importable regardless of caller's cwd
from hash_workload import hash_many  # noqa: E402  # => co-13: the function under profiling, unchanged from hash_workload.py


def main() -> (
    None
):  # => co-13/co-22: profiles hash_many() and confirms the C-extension call is exactly one opaque line
    profiler = cProfile.Profile()  # => co-13: a fresh Profile() instance, not the module-level cProfile.run() shortcut
    profiler.enable()  # => co-13: starts intercepting every call/return event from this point on
    hash_many(
        b"payload" * 64, times=200_000
    )  # => co-13: enough repetitions that the C call genuinely dominates the run
    profiler.disable()  # => co-13: stops intercepting -- exact per-call counts are now frozen

    buf = StringIO()  # => co-13: captures pstats' own printed table for later inspection, instead of only stdout
    stats = pstats.Stats(profiler, stream=buf).sort_stats(
        pstats.SortKey.CUMULATIVE
    )  # => co-13: sorted by cumulative time
    stats.print_stats(
        5
    )  # => co-13: the top 5 entries -- enough to show the C-extension line among the Python ones
    output = (
        buf.getvalue()
    )  # => co-13: the actual printed text, read back for the assertion below
    print(
        output
    )  # => co-13: also prints it for a human reader, same content as the assertion checks

    # co-13/co-22: confirm the C-extension call appears as exactly ONE line --
    # no sub-function breakdown of anything happening inside OpenSSL is visible.
    sha256_lines = [
        line for line in output.splitlines() if "sha256" in line
    ]  # => co-13: filters for the C-extension's own row
    assert len(sha256_lines) == 1, (
        f"expected exactly one opaque sha256 line, found {len(sha256_lines)}"
    )  # => co-13: the real check
    print(
        f"confirmed: cProfile shows exactly one opaque line for the C extension call: {sha256_lines[0].strip()}"
    )  # => co-13
    print(  # => co-22: explains what a native-aware profiler WOULD add, and why none is available on this host
        "the ONLY way to see what happens INSIDE that C call (e.g. which OpenSSL "  # => co-22: message part 1
        "internal routine dominates) is a native-aware profiler like `perf record` "  # => co-22: message part 2
        "or `py-spy record --native` -- both unavailable on this host (perf is "  # => co-22: message part 3
        "Linux-only; py-spy requires root on macOS, confirmed in ex-29/ex-71)."  # => co-22: message part 4 -- closes the print
    )  # => co-22: closes the multi-line print call


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that profiles, verifies, and explains in one run
