"""Example 80: a minimal line tracer built with sys.settrace, and an equivalent
one built with sys.monitoring -- measure real wall time for each over the SAME
workload, and confirm sys.monitoring's overhead is measurably lower.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the comparison itself

import sys  # => co-22: both sys.settrace and sys.monitoring live directly on this module
import time  # => co-22/co-23: time.perf_counter() measures REAL wall time for each tracer, plus an untraced baseline

sys.path.insert(
    0, "."
)  # => makes local workload.py importable regardless of caller's cwd
from workload import compute  # noqa: E402  # => co-22: the SAME function traced by BOTH mechanisms, for a fair comparison

LINE_COUNTS: dict[
    int, int
] = {}  # => co-22: populated by the sys.settrace tracer below -- one entry per traced line


def settrace_line_tracer(
    frame: object, event: str, arg: object
) -> object:  # => co-22: the PER-LINE local tracer sys.settrace calls
    if (
        event == "line"
    ):  # => co-22: fires on EVERY line executed inside the traced call -- the expensive part
        LINE_COUNTS[frame.f_lineno] = LINE_COUNTS.get(frame.f_lineno, 0) + 1  # type: ignore[attr-defined]  # => co-22: tallies hits per line
    return settrace_line_tracer  # => co-22: must return itself to keep receiving "line" events for this frame


def settrace_tracer_wrapper(
    frame: object, event: str, arg: object
) -> object:  # => co-22: the GLOBAL tracer sys.settrace registers
    # co-22: sys.settrace needs a per-CALL "global" tracer that returns a
    # per-line local tracer -- this is the classic two-level trace-function API.
    if (
        event == "call"
    ):  # => co-22: fires ONCE per function call -- the entry point into the two-level API
        return settrace_line_tracer  # => co-22: hands off to the per-line tracer for THIS specific call's frame
    return None  # => co-22: no local tracer for any other top-level event type


MONITORING_LINE_COUNTS: dict[
    int, int
] = {}  # => co-22: populated by the sys.monitoring callback below -- the AFTER-side tally
TOOL_ID = (
    sys.monitoring.PROFILER_ID
)  # => co-22: reserves ONE of sys.monitoring's fixed tool-id slots for this example


def monitoring_line_callback(
    code: object, line: int
) -> None:  # => co-22: sys.monitoring's OWN per-line callback shape
    MONITORING_LINE_COUNTS[line] = (
        MONITORING_LINE_COUNTS.get(line, 0) + 1
    )  # => co-22: the SAME tally logic as LINE_COUNTS above


def run_with_settrace(
    n: int,
) -> float:  # => co-22: times compute(n) under the sys.settrace-based tracer
    LINE_COUNTS.clear()  # => co-22: resets the tally so each run starts from zero, independent of prior runs
    sys.settrace(
        settrace_tracer_wrapper
    )  # => co-22: installs the GLOBAL tracer -- every subsequent call gets traced
    start = time.perf_counter()  # => co-22: starts timing AFTER the tracer is installed -- measures traced execution only
    compute(
        n
    )  # => co-22: the SAME workload run_with_monitoring() below will also call, for a fair comparison
    elapsed = (
        time.perf_counter() - start
    )  # => co-22: the REAL wall time for n iterations, WITH sys.settrace active
    sys.settrace(None)  # => co-22: always disable, even on error, in real code
    return elapsed  # => co-22: the settrace-traced elapsed time, compared against monitoring's below


def run_with_monitoring(
    n: int,
) -> float:  # => co-22: times compute(n) under the sys.monitoring-based tracer
    MONITORING_LINE_COUNTS.clear()  # => co-22: resets the tally so each run starts from zero
    sys.monitoring.use_tool_id(
        TOOL_ID, "example-80-tracer"
    )  # => co-22: registers this example as the owner of TOOL_ID
    sys.monitoring.register_callback(
        TOOL_ID, sys.monitoring.events.LINE, monitoring_line_callback
    )  # => co-22: wires the callback
    sys.monitoring.set_local_events(
        TOOL_ID, compute.__code__, sys.monitoring.events.LINE
    )  # => co-22: scoped to compute() ONLY
    start = time.perf_counter()  # => co-22: starts timing AFTER instrumentation is installed -- measures traced execution only
    compute(
        n
    )  # => co-22: the SAME workload run_with_settrace() above also called, for a fair comparison
    elapsed = (
        time.perf_counter() - start
    )  # => co-22: the REAL wall time for n iterations, WITH sys.monitoring active
    sys.monitoring.set_local_events(
        TOOL_ID, compute.__code__, sys.monitoring.events.NO_EVENTS
    )  # => co-22: stops future line events
    sys.monitoring.register_callback(
        TOOL_ID, sys.monitoring.events.LINE, None
    )  # => co-22: unregisters the callback cleanly
    sys.monitoring.free_tool_id(
        TOOL_ID
    )  # => co-22: releases TOOL_ID -- good hygiene, avoids leaking the fixed slot
    return elapsed  # => co-22: the monitoring-traced elapsed time, compared against settrace's above


def main() -> (
    None
):  # => co-22/co-23: runs baseline, settrace, and monitoring, and confirms monitoring's overhead is lower
    n = 300_000  # => co-22: large enough that per-line tracing overhead is clearly visible against the untraced baseline

    baseline_start = (
        time.perf_counter()
    )  # => co-22: the UNTRACED baseline -- no tracer installed at all
    compute(
        n
    )  # => co-22: the SAME n as both traced runs below, for a fair three-way comparison
    baseline = (
        time.perf_counter() - baseline_start
    )  # => co-22: the REAL wall time with NO tracing overhead whatsoever
    print(
        f"no tracer at all (baseline):  {baseline * 1000:.1f}ms"
    )  # => co-22: the reference point both overheads are measured against

    settrace_elapsed = run_with_settrace(
        n
    )  # => co-22: the classic, two-level trace-function mechanism
    print(
        f"sys.settrace line tracer:      {settrace_elapsed * 1000:.1f}ms ({len(LINE_COUNTS)} distinct lines seen)"
    )  # => co-22

    monitoring_elapsed = run_with_monitoring(
        n
    )  # => co-22: PEP 669's purpose-built low-overhead alternative
    print(  # => co-22: prints the monitoring result, with the SAME "distinct lines seen" sanity check as settrace above
        f"sys.monitoring line tracer:    {monitoring_elapsed * 1000:.1f}ms "  # => co-22: message part 1
        f"({len(MONITORING_LINE_COUNTS)} distinct lines seen)"  # => co-22: message part 2, closes the print
    )  # => co-22: closes the multi-line print call

    settrace_overhead = (
        settrace_elapsed - baseline
    )  # => co-22: settrace's COST above the untraced baseline, isolated
    monitoring_overhead = (
        monitoring_elapsed - baseline
    )  # => co-22: monitoring's COST above the SAME untraced baseline
    print(
        f"sys.settrace overhead:   {settrace_overhead * 1000:.1f}ms"
    )  # => co-22: the BEFORE number, for the final comparison
    print(
        f"sys.monitoring overhead: {monitoring_overhead * 1000:.1f}ms"
    )  # => co-22: the AFTER number, for the final comparison

    assert monitoring_overhead < settrace_overhead, (
        "expected sys.monitoring's overhead to be measurably lower"
    )  # => co-22/co-23
    print(  # => co-22/co-23: the headline result -- HOW MANY TIMES lower, not just "lower"
        f"confirmed: sys.monitoring's overhead is {settrace_overhead / max(monitoring_overhead, 1e-9):.1f}x "  # => co-22: message part 1
        "lower than sys.settrace's, for the identical line-tracing job"  # => co-22: message part 2, closes the print
    )  # => co-22: closes the multi-line print call


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that measures baseline, settrace, and monitoring, and reports the comparison
