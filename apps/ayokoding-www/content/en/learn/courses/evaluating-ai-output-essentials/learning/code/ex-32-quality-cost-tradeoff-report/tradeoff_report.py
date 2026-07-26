# learning/code/ex-32-quality-cost-tradeoff-report/tradeoff_report.py
"""Worked Example 32: Quality/Cost Trade-off Report."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import NamedTuple  # => co-11: a typed record for one run's combined quality/cost/latency summary


class RunSummary(NamedTuple):  # => co-11: pass rate, cost, and latency -- reported TOGETHER, never separately
    pass_rate: float  # => co-07: the headline quality number
    cost_usd: float  # => co-11: the headline cost number, for the SAME run
    p95_latency_ms: float  # => co-11: the headline latency number, for the SAME run


BASELINE = RunSummary(pass_rate=0.83, cost_usd=0.012, p95_latency_ms=480.0)  # => co-09: "prompt v1" -- the current shipped version
CANDIDATE = RunSummary(pass_rate=1.00, cost_usd=0.048, p95_latency_ms=910.0)  # => co-09: "prompt v2" -- a proposed change


def render_tradeoff(baseline: RunSummary, candidate: RunSummary) -> str:  # => co-11: one report, three deltas, side by side
    """Render pass-rate, cost, and latency deltas between `baseline` and `candidate`."""  # => co-11: documents render_tradeoff's contract -- no runtime output, just sets its __doc__
    pass_delta = candidate.pass_rate - baseline.pass_rate  # => co-07: the quality change
    cost_ratio = candidate.cost_usd / baseline.cost_usd  # => co-11: the cost change, as a multiplier
    latency_delta = candidate.p95_latency_ms - baseline.p95_latency_ms  # => co-11: the latency change, in milliseconds
    return (  # => co-11: assembles the three deltas into one printable report
        f"Pass rate: {baseline.pass_rate:.0%} -> {candidate.pass_rate:.0%} ({pass_delta:+.0%})\n"  # => co-07: quality line
        f"Cost: ${baseline.cost_usd:.3f} -> ${candidate.cost_usd:.3f} ({cost_ratio:.1f}x)\n"  # => co-11: cost line
        f"p95 latency: {baseline.p95_latency_ms:.0f}ms -> {candidate.p95_latency_ms:.0f}ms ({latency_delta:+.0f}ms)"  # => co-11: latency line
    )  # => co-11: closes the assembled report string


if __name__ == "__main__":  # => co-11: entry point -- runs only when this file executes directly, not on import
    report = render_tradeoff(BASELINE, CANDIDATE)  # => co-11: build the whole trade-off report in one call
    print(report)  # => co-11: prints all three deltas together
    quality_improved = CANDIDATE.pass_rate > BASELINE.pass_rate  # => co-07: is this candidate a quality win?
    cost_regressed = CANDIDATE.cost_usd >= 4 * BASELINE.cost_usd  # => co-11: is this candidate a real cost regression?
    print(f"Quality improved: {quality_improved} | Cost regressed 4x+: {cost_regressed}")  # => co-11: states both facts plainly
    assert quality_improved, "the candidate must genuinely improve pass rate for this scenario"  # => co-07: confirms the win
    assert cost_regressed, "the candidate must genuinely cost 4x or more for this scenario"  # => co-11: confirms the trade
    print("MATCH: a 17-point quality win paid for with a 4x cost increase is a DECISION, not a free lunch")  # => co-11
    # => co-11: without this report, only the pass-rate line would ship the change -- the cost line is what makes it a choice
