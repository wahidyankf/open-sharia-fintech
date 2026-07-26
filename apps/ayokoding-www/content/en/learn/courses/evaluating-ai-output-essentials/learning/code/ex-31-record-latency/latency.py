# learning/code/ex-31-record-latency/latency.py
"""Worked Example 31: Record Latency."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import statistics  # => co-11: quantiles need nothing beyond the standard library's own statistics module

CASE_LATENCIES_MS = {  # => co-11: mocked, fixed per-case latencies in milliseconds -- no live network call needed
    "case-01": 420,  # => co-11: fast
    "case-02": 455,  # => co-11: fast
    "case-03": 402,  # => co-11: fast
    "case-04": 610,  # => co-11: cases 1-4 -- mostly fast
    "case-05": 398,  # => co-11: fast
    "case-06": 441,  # => co-11: fast
    "case-07": 415,  # => co-11: fast
    "case-08": 590,  # => co-11: cases 5-8 -- one more slow outlier
    "case-09": 407,  # => co-11: fast
    "case-10": 388,  # => co-11: fast
    "case-11": 433,  # => co-11: fast
    "case-12": 449,  # => co-11: cases 9-12 -- back to typical speed
}  # => co-11: closes CASE_LATENCIES_MS -- twelve fixed, reproducible latency samples


def p95(latencies_ms: list[int]) -> float:  # => co-11: the 95th percentile -- the near-worst-case, not the average
    """Return the 95th-percentile value of `latencies_ms`."""  # => co-11: documents p95's contract -- no runtime output, just sets its __doc__
    return statistics.quantiles(latencies_ms, n=100)[94]  # => co-11: n=100 quantiles -- index 94 is the 95th percentile cut


if __name__ == "__main__":  # => co-11: entry point -- runs only when this file executes directly, not on import
    latencies = list(CASE_LATENCIES_MS.values())  # => co-11: this run's twelve latency samples, in dataset order
    mean_latency = statistics.mean(latencies)  # => co-11: the average -- easily hidden by one slow outlier
    p95_latency = p95(latencies)  # => co-11: the tail -- what most users near the slow end actually experience
    print(f"Mean latency: {mean_latency:.1f} ms")  # => co-11: prints the average
    print(f"p95 latency: {p95_latency:.1f} ms")  # => co-11: prints the near-worst-case figure
    assert mean_latency < p95_latency, "the p95 figure must sit above the mean whenever an outlier exists"  # => co-11
    print("MATCH: the p95 figure exposes the outlier the mean alone would hide")  # => co-11
    # => co-11: recording BOTH mean and p95 alongside pass rate is what turns "it feels slower" into a comparable number
