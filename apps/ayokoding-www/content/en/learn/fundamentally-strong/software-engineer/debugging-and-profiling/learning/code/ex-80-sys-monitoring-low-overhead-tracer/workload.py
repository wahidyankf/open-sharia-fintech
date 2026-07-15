"""Example 80: a plain CPU-bound workload traced two ways -- sys.settrace's
line-by-line callback (the classic, expensive mechanism pdb itself is built on)
vs sys.monitoring (PEP 669, Python 3.12+), which is designed for exactly this
low-overhead-tracing use case.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to tracing itself


def compute(
    n: int,
) -> int:  # => co-22/co-23: the ONE function BOTH tracers instrument, so their overhead is directly comparable
    total = 0  # => co-22: accumulator -- its final value is irrelevant, only the TRACED WORK matters here
    for i in range(
        n
    ):  # => co-22: n iterations -- each one fires a "line" event under BOTH tracing mechanisms
        total += (
            i * i
        )  # => co-22: cheap per-iteration math -- keeps this CPU-bound, so tracer overhead genuinely shows up
    return total  # => co-22: discarded by every caller -- only the ELAPSED TIME under each tracer is measured
