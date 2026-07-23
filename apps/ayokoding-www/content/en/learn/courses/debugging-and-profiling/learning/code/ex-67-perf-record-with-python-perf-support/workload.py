"""Example 67: the workload `perf record -F 99 -g` would sample, using CPython's
`-X perf` support (PEP 799-adjacent; a real, working CPython flag on ANY OS --
it just has nothing to attach to without the Linux `perf` tool itself).
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to perf itself


def hot_function(
    n: int,
) -> int:  # => co-22: the ONE function perf's `-g` (call-graph) sampling would name in its report
    return sum(
        i * i for i in range(n)
    )  # => co-22: real CPU work -- long enough for a 99Hz sampler to catch several hits


def main() -> (
    None
):  # => co-22: one frame above hot_function() -- also visible in perf's own call graph, if it ran
    hot_function(
        2_000_000
    )  # => co-22: large enough that hot_function dominates the run, same shape as other tiers


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => co-22: the ONE call `python -X perf` + `perf record` would sample against on a Linux host
