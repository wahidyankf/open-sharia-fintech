"""Capstone step 3b: sampling profile (mini_sampler, since py-spy needs root on
this host -- see ex-29/ex-71) of the SAME pipeline -- an INDEPENDENT method that
must agree with cProfile's instrumenting result on the hot spot.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to sampling itself

import sys  # => needed only for sys.path.insert below
import threading  # => co-14: threading.get_ident() -- the CURRENT thread's id, sampled from itself

sys.path.insert(
    0, "."
)  # => makes local make_large_batch.py/mini_sampler.py/pipeline.py importable
from make_large_batch import make_large_batch  # noqa: E402  # => co-19: the SAME batch step 3a's instrumenting profile also used
from mini_sampler import collect_samples  # noqa: E402  # => co-14: reuses ex-30's disclosed py-spy substitute, unchanged
from pipeline import build_customer_report  # noqa: E402  # => co-19: the SAME pipeline, profiled a SECOND, independent way


def main() -> (
    None
):  # => co-19/co-14: samples the SAME pipeline and confirms the SAME hot spot, independently
    orders = (
        make_large_batch()
    )  # => co-19: the SAME 60,000-order batch step 3a's cProfile run also profiled

    def run() -> (
        None
    ):  # => co-14: the exact callable mini_sampler.collect_samples() will invoke and sample
        build_customer_report(
            orders
        )  # => co-19: the SAME pipeline call cProfile instrumented in step 3a

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
    total = sum(
        leaf_counts.values()
    )  # => co-19: denominator for turning the widest count into a percentage
    widest = max(
        leaf_counts.items(), key=lambda kv: kv[1]
    )  # => co-19: the single widest frame, by sample count
    print(
        f"sampling profile collected {total} samples across {len(leaf_counts)} distinct leaf frames"
    )  # => co-19
    print(
        f"sampling profile's widest frame: {widest[0]!r} -- {widest[1]}/{total} samples ({widest[1] / total:.1%})"
    )  # => co-19

    assert widest[0] == "dedupe_customers", (
        f"expected dedupe_customers to be the widest frame, got {widest[0]!r}"
    )  # => co-19: real check
    print(
        "confirmed: BOTH the instrumenting profile (cProfile) and the sampling profile (mini_sampler)"
    )  # => co-19/co-13
    print(
        "independently agree that dedupe_customers is the hot spot"
    )  # => co-19/co-13: the payoff -- two methods, one answer


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that samples, verifies, and confirms agreement with the instrumenting profile
