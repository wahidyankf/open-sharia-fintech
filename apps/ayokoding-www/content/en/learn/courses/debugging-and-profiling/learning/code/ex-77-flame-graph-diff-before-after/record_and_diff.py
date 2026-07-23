"""Example 77: record BEFORE and AFTER folded stacks (via mini_sampler, since
py-spy needs root here) for a real flame-graph-diff SVG, AND cross-check the
"wide frame shrank, nothing else grew" property with cProfile's own numbers --
the leaf FUNCTION NAME (`validate_row`) is identical in both versions (only its
internal data structure changed, list vs set), so a leaf-name-only flame-graph
comparison can't tell the two apart on its own; tottime SHARE can.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import cProfile  # => co-19/co-23: the SAME instrumenting profiler used to compute tottime shares below
import importlib  # => co-19: loads workload_before/workload_after by NAME, so one function covers both
import pstats  # => co-19: turns cProfile's raw stats into per-function tottime numbers
import sys  # => needed only for sys.path.insert below
import threading  # => co-19: threading.get_ident() -- the CURRENT thread's id, sampled from itself, same as ex-53

sys.path.insert(
    0, "."
)  # => makes local mini_sampler.py/workload_before.py/workload_after.py importable
from mini_sampler import collect_samples  # noqa: E402  # => co-19: reuses ex-30's disclosed py-spy substitute, unchanged


def make_rows(
    n_rows: int,
) -> list[
    dict[str, str]
]:  # => co-19: builds the SAME input shape for BOTH BEFORE and AFTER
    return [
        {"id": f"id-{i % (n_rows // 3 + 1)}", "extra": "x" * 20} for i in range(n_rows)
    ]  # => co-19: repeated ids -- real duplicates


def record_folded_stacks(
    module_name: str, rows: list[dict[str, str]], repeat: int, out_path: str
) -> None:  # => co-19: one recording pass
    # co-19: same microbenchmark-repeat trick as ex-48/ex-53 -- gives the fast
    # AFTER version a sampleable window comparable to the naturally-slow BEFORE.
    module = importlib.import_module(
        module_name
    )  # => co-19: dynamically loads "workload_before" or "workload_after"

    def run() -> (
        None
    ):  # => co-19: the exact callable mini_sampler.collect_samples() will invoke and sample
        for _ in range(
            repeat
        ):  # => co-19: repeats `repeat` times -- 1x for the naturally-slow BEFORE, 400x for the fast AFTER
            module.pipeline(
                rows
            )  # => co-19: the SAME workload.pipeline() shape, whichever module was requested

    samples = collect_samples(
        run, threading.get_ident(), interval_s=0.0005
    )  # => co-19: real samples, real stacks
    with (
        open(out_path, "w") as f
    ):  # => co-19: the collapsed-stack text format inferno-flamegraph/inferno-diff-folded read
        for (
            stack,
            count,
        ) in samples.items():  # => co-19: one line per distinct stack shape
            f.write(
                f"{stack} {count}\n"
            )  # => co-19: "frame;frame;frame count" -- the exact folded-stack format
    print(
        f"{module_name}: wrote {sum(samples.values())} samples to {out_path}"
    )  # => co-19: confirms the file was written


def tottime_share(
    module_name: str, rows: list[dict[str, str]], funcname: str
) -> tuple[float, float]:  # => co-19/co-23: cross-checks vs cProfile
    module = importlib.import_module(
        module_name
    )  # => co-19: the SAME dynamic import as record_folded_stacks() above
    profiler = cProfile.Profile()  # => co-19: a fresh Profile() instance per call
    profiler.enable()  # => co-19: starts intercepting every call/return event
    module.pipeline(
        rows
    )  # => co-19: the SAME rows, run through whichever module was requested
    profiler.disable()  # => co-19: stops intercepting -- exact per-call counts are now frozen
    stats = pstats.Stats(
        profiler
    )  # => co-19: wraps the raw profile in pstats' queryable form
    target_tt, total_tt = (
        0.0,
        0.0,
    )  # => co-19: tracks funcname's OWN tottime and the run's TOTAL tottime
    for (_fn, _ln, name), entry in stats.stats.items():  # type: ignore[attr-defined]  # => co-19: one entry per profiled function
        total_tt += entry[
            2
        ]  # => co-19: accumulates every function's own tottime into the run's total
        if (
            name == funcname
        ):  # => co-19: filters for the ONE function this call was asked to measure
            target_tt = entry[
                2
            ]  # => co-19: entry[2] is tottime -- this function's OWN time, not its callees'
    return (
        target_tt,
        total_tt,
    )  # => co-19/co-23: both numbers the caller needs for a share percentage


def main() -> (
    None
):  # => co-19/co-23: records folded stacks for the flame-graph diff, and cross-checks with cProfile
    rows = make_rows(
        n_rows=20_000
    )  # => co-19: the SAME 20,000-row input for both mini_sampler AND cProfile passes

    record_folded_stacks(
        "workload_before", rows, repeat=1, out_path="before.collapsed"
    )  # => co-19: the SLOW O(n^2) version
    record_folded_stacks(
        "workload_after", rows, repeat=400, out_path="after.collapsed"
    )  # => co-19: the FAST O(n) version, repeated

    before_tt, before_total = tottime_share(
        "workload_before", rows, "validate_row"
    )  # => co-19: BEFORE's own leaf tottime share
    after_tt, after_total = tottime_share(
        "workload_after", rows, "validate_row"
    )  # => co-19: AFTER's own leaf tottime share
    before_share = (
        before_tt / before_total
    )  # => co-19: validate_row's SHARE of the total BEFORE
    after_share = (
        after_tt / after_total
    )  # => co-19: validate_row's SHARE of the total AFTER -- should be much smaller
    print(
        f"validate_row tottime share:      BEFORE {before_share:.1%} -> AFTER {after_share:.1%}"
    )  # => co-19: the headline comparison

    before_stable_tt, _ = tottime_share(
        "workload_before", rows, "other_stable_work"
    )  # => co-23: the REGRESSION CHECK, BEFORE
    after_stable_tt, _ = tottime_share(
        "workload_after", rows, "other_stable_work"
    )  # => co-23: the REGRESSION CHECK, AFTER
    print(
        f"other_stable_work absolute tottime: BEFORE {before_stable_tt * 1e6:.1f}us -> AFTER {after_stable_tt * 1e6:.1f}us"
    )  # => co-23

    assert after_share < before_share, (
        "expected validate_row's tottime SHARE (the wide frame) to shrink"
    )  # => co-19: the real check
    assert after_stable_tt < before_stable_tt * 2, (
        "expected other_stable_work to NOT have grown"
    )  # => co-23: the real check
    print(
        "confirmed: the wide frame shrank proportionally after the fix, and nothing else grew"
    )  # => co-19/co-23: the payoff


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that records, cross-checks, and confirms in one run
