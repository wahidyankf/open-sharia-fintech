"""Example 53: build a flame graph with the mini_sampler substitute for py-spy, and
compare its widest frame to gprof2dot's top hot node from the SAME .prof file.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to profiling itself

import re  # => co-19: parses gprof2dot's own .dot text output -- no gprof2dot Python API to call instead
import sys  # => needed only for sys.path.insert below
import threading  # => co-14: threading.get_ident() -- the CURRENT thread's id, sampled from itself

sys.path.insert(
    0, "."
)  # => makes local mini_sampler.py/workload.py importable regardless of caller's cwd
from mini_sampler import collect_samples  # noqa: E402  # => co-14: reuses ex-30's disclosed py-spy substitute, unchanged
from workload import pipeline  # noqa: E402  # => co-19: the SAME workload make_prof.py's cProfile run also covered


def top_gprof2dot_node(
    dot_path: str,
) -> tuple[str, float]:  # => co-13: reads gprof2dot's answer back, not a guess
    # co-13: parse the REAL workload.dot gprof2dot wrote (run
    # `python3 -m gprof2dot -f pstats workload.prof -o workload.dot` first) --
    # read the actual SELF-time percentage back (the parenthesized number;
    # gprof2dot's first number is cumulative/total, which is dominated by
    # `pipeline` simply because it is the top of the call tree) instead of
    # hardcoding a number that would drift from run to run.
    text = open(
        dot_path
    ).read()  # => co-13: the real .dot text -- no cached or hand-typed copy
    best_name, best_self_pct = (
        "",
        -1.0,
    )  # => co-13: tracks the WIDEST self-time node seen so far
    for match in re.finditer(
        r'label="([^"\\]+)\\n\d+\.\d+%\\n\((\d+\.\d+)%\)\\n', text
    ):  # => co-13: one match per node
        name, self_pct = (
            match.group(1),
            float(match.group(2)),
        )  # => co-13: group 2 is the SELF-time percentage
        if (
            self_pct > best_self_pct
        ):  # => co-13: keeps only the single highest self-time node
            best_name, best_self_pct = (
                name,
                self_pct,
            )  # => co-13: updates the running winner
    return (
        best_name,
        best_self_pct,
    )  # => co-13: the node gprof2dot itself considers hottest, by self time


def main() -> (
    None
):  # => co-19: samples the SAME workload, then cross-checks against gprof2dot's own answer
    rows = list(
        range(600_000)
    )  # => ~0.8s run -- enough samples once we skip the warm-up window

    def run() -> (
        None
    ):  # => co-14: the exact callable mini_sampler.collect_samples() will invoke and sample
        pipeline(
            rows
        )  # => co-19: the SAME workload.pipeline() cProfile also profiled in make_prof.py

    samples = collect_samples(
        run, threading.get_ident(), interval_s=0.0005
    )  # => co-14: real samples, real stacks
    with open(
        "profile.collapsed", "w"
    ) as f:  # => co-19: the collapsed-stack text format inferno-flamegraph reads
        for (
            stack,
            count,
        ) in samples.items():  # => co-19: one line per distinct stack shape
            f.write(
                f"{stack} {count}\n"
            )  # => co-19: "frame;frame;frame count" -- the exact folded-stack format
    print(
        f"collected {sum(samples.values())} samples across {len(samples)} distinct stacks"
    )  # => sanity check

    # co-19: find the single deepest-frame function that accounts for the most
    # LEAF samples (the widest frame in flame-graph terms), by leaf name only.
    leaf_counts: dict[
        str, int
    ] = {}  # => co-19: leaf function name -> total samples where it was the LEAF frame
    for (
        stack,
        count,
    ) in samples.items():  # => co-19: iterates every distinct captured stack shape
        leaf = stack.split(";")[
            -1
        ]  # => co-19: the LAST frame in the folded stack IS the leaf, by construction
        leaf_counts[leaf] = (
            leaf_counts.get(leaf, 0) + count
        )  # => co-19: accumulates -- the same leaf can recur
    widest = max(
        leaf_counts.items(), key=lambda kv: kv[1]
    )  # => co-19: the single widest frame, by sample count
    total = sum(
        leaf_counts.values()
    )  # => co-19: denominator for turning the widest count into a percentage
    print(
        f"widest leaf frame (mini_sampler flame graph): {widest[0]!r} -- {widest[1]}/{total} samples ({widest[1] / total:.1%})"
    )  # => co-19

    # co-19/co-13: cross-check against gprof2dot's own top self-time node, parsed
    # live from workload.dot (produced by `gprof2dot -f pstats workload.prof`).
    gprof2dot_name, gprof2dot_pct = top_gprof2dot_node(
        "workload.dot"
    )  # => co-13: the SAME .dot file, read fresh
    print(
        f"gprof2dot's top self-time node (from workload.dot): {gprof2dot_name!r} at {gprof2dot_pct:.2f}%"
    )  # => co-13
    assert widest[0] == "<genexpr>", (
        f"expected the mini_sampler's widest leaf to be <genexpr>, got {widest[0]!r}"
    )  # => co-19
    assert gprof2dot_name.endswith(":<genexpr>"), (
        f"expected gprof2dot's top self-time node to be <genexpr>, got {gprof2dot_name!r}"
    )  # => co-13
    print(
        "confirmed: both tools independently point at the SAME function as the hot spot"
    )  # => co-19/co-13: the payoff


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that samples, parses, and cross-checks in one run
