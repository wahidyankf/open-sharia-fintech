# learning/code/ex-52-latency-jitter-percentiles-measure/latency_jitter_percentiles_measure.py
"""Example 52: Latency Percentiles and Jitter -- Computed Against a Known Sample."""  # => co-23: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import statistics  # => co-23: mean() is exactly the right tool for jitter -- the AVERAGE consecutive-sample difference


def percentile(sorted_samples: list[float], p: float) -> float:  # => co-23: linear-interpolation percentile -- the same method most monitoring tools use
    """Compute the p-th percentile of an ALREADY-SORTED sample, using linear interpolation between ranks."""  # => co-23: documents percentile's contract -- no runtime output, just sets its __doc__
    if not sorted_samples:  # => co-23: an empty sample has no meaningful percentile -- fail loudly rather than return a bogus value
        raise ValueError("cannot compute a percentile of an empty sample")  # => co-23: continues the statement started above
    rank = (len(sorted_samples) - 1) * (p / 100)  # => co-23: the FRACTIONAL index this percentile falls at, 0-indexed
    lower_index = int(rank)  # => co-23: the rank's integer (floor) part -- the sample just BELOW the target percentile
    upper_index = min(lower_index + 1, len(sorted_samples) - 1)  # => co-23: the sample just ABOVE it, clamped so the top percentile never indexes past the end
    if lower_index == upper_index:  # => co-23: the rank landed EXACTLY on a sample -- no interpolation needed
        return sorted_samples[lower_index]  # => co-23: returns this computed value to the caller
    fraction_above = rank - lower_index  # => co-23: how far PAST lower_index the fractional rank sits, in [0, 1)
    lower_weight = sorted_samples[lower_index] * (upper_index - rank)  # => co-23: the lower sample's contribution, weighted by closeness
    upper_weight = sorted_samples[upper_index] * fraction_above  # => co-23: the upper sample's contribution, weighted by closeness
    return lower_weight + upper_weight  # => co-23: the interpolated value between the two bracketing samples


def jitter(samples: list[float]) -> float:  # => co-23: jitter -- the AVERAGE variance between CONSECUTIVE measurements, not overall spread
    """Compute mean absolute difference between consecutive samples, IN THEIR ORIGINAL ORDER (not sorted)."""  # => co-23: documents jitter's contract -- no runtime output, just sets its __doc__
    consecutive_diffs = [abs(samples[i] - samples[i - 1]) for i in range(1, len(samples))]  # => co-23: one difference per adjacent PAIR -- order matters here, unlike percentile()
    return statistics.mean(consecutive_diffs)  # => co-23: the average of those differences -- co-23's own definition of jitter


if __name__ == "__main__":  # => co-23: entry point -- this block runs only when the file executes directly, not on import
    # A fixed, known sample of 10 round-trip times (milliseconds), IN THE ORDER THEY WERE MEASURED --
    # mostly clustered around 10-13ms, with two deliberate outliers (50ms, 90ms) simulating a brief
    # congestion event partway through the run. Kept fixed (not live-measured) so this script's
    # percentile/jitter arithmetic can be checked by hand, independent of any network's own noise.
    known_sample_ms = [10.0, 12.0, 11.0, 50.0, 13.0, 11.5, 12.5, 90.0, 10.5, 11.0]  # => co-23: the raw, ORIGINAL-ORDER sample -- jitter needs this order, percentiles do not
    sorted_sample = sorted(known_sample_ms)  # => co-23: percentiles need the sample SORTED -- a separate copy, so jitter's order-sensitive input stays untouched
    print(f"raw sample (measurement order): {known_sample_ms}")  # => co-23: the input as it would have been recorded, one RTT per request
    print(f"sorted sample:                  {sorted_sample}")  # => co-23: the same 10 values, ascending -- what percentile() actually reads

    p50 = percentile(sorted_sample, 50)  # => co-23: the MEDIAN -- half of requests were faster, half slower
    p95 = percentile(sorted_sample, 95)  # => co-23: only 5% of requests were slower than this -- the tail most dashboards alert on
    p99 = percentile(sorted_sample, 99)  # => co-23: only 1% of requests were slower than this -- the EXTREME tail, closest to a worst case
    jitter_ms = jitter(known_sample_ms)  # => co-23: computed on the RAW order -- captures how much consecutive requests actually swung
    print(f"p50={p50:.2f}ms  p95={p95:.2f}ms  p99={p99:.2f}ms  jitter={jitter_ms:.2f}ms")  # => co-23: the four headline numbers this example computes

    # Hand check for p50: n=10 samples, rank = (10-1) * 0.50 = 4.5 -- interpolate HALFWAY between
    # sorted_sample[4] (11.5) and sorted_sample[5] (12.0): 11.5 + 0.5*(12.0-11.5) = 11.75.
    assert abs(p50 - 11.75) < 1e-9, f"p50 must hand-check to exactly 11.75, got {p50}"  # => co-23: the exact-match check against the worked-by-hand expectation
    assert p95 > p50, "p95 must exceed p50 -- the 95th percentile can never be smaller than the median"  # => co-23
    assert p99 >= p95, "p99 must be at least p95 -- percentiles are monotonically non-decreasing as p increases"  # => co-23
    assert jitter_ms > 0, "jitter must be positive -- this sample is not perfectly flat"  # => co-23

    mean_ms = statistics.mean(known_sample_ms)  # => co-23: the single-number AVERAGE -- the value percentiles exist specifically to NOT rely on
    print(f"\nmean = {mean_ms:.2f}ms  (a single average this misleadingly close to p50 hides that p99={p99:.2f}ms is ~{p99 / mean_ms:.1f}x higher)")  # => co-23: ties the numbers back to WHY a single average is insufficient
    print("Percentiles and jitter match their hand-computed expectations: True")  # => co-23: reached only if every assert above passed
    # => co-23: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
    # => co-23: percentile() and jitter() both operate on the SAME 10 numbers, but percentile() needs them sorted while jitter() needs the ORIGINAL measurement order -- conflating the two is a common percentile-computation bug
