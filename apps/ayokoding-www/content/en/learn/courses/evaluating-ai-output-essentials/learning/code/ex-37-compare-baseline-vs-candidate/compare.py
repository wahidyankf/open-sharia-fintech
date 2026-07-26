# learning/code/ex-37-compare-baseline-vs-candidate/compare.py
"""Worked Example 37: Compare Baseline vs. Candidate."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

BASELINE = {"case-A": True, "case-B": False, "case-C": True, "case-D": True, "case-E": False}  # => co-09: five cases, two failing
CANDIDATE = {"case-A": True, "case-B": True, "case-C": True, "case-D": False, "case-E": False}  # => co-09: SAME five cases, changed


def diff_runs(baseline: dict[str, bool], candidate: dict[str, bool]) -> tuple[list[str], list[str]]:  # => co-09: one diff, two lists
    """Return (wins, regressions) -- case ids that flipped False->True, and True->False, respectively."""  # => co-09: documents diff_runs's contract -- no runtime output, just sets its __doc__
    wins = [cid for cid in baseline if not baseline[cid] and candidate[cid]]  # => co-09: failed before, passes now
    regressions = [cid for cid in baseline if baseline[cid] and not candidate[cid]]  # => co-09: passed before, fails now
    return wins, regressions  # => co-09: returns this computed value to the caller


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    wins, regressions = diff_runs(BASELINE, CANDIDATE)  # => co-09: one call produces both lists, cleanly separated
    baseline_rate = sum(BASELINE.values()) / len(BASELINE)  # => co-07: the baseline's headline number
    candidate_rate = sum(CANDIDATE.values()) / len(CANDIDATE)  # => co-07: the candidate's headline number
    print(f"Baseline pass rate: {baseline_rate:.0%} | Candidate pass rate: {candidate_rate:.0%}")  # => co-07: prints both headlines
    print(f"Wins (fixed): {wins}")  # => co-09: prints exactly which cases newly pass
    print(f"Regressions (broken): {regressions}")  # => co-09: prints exactly which cases newly fail
    assert wins == ["case-B"], "exactly case-B must be a win -- it flipped fail-to-pass"  # => co-09: confirms the win list
    assert regressions == ["case-D"], "exactly case-D must be a regression -- it flipped pass-to-fail"  # => co-09
    assert baseline_rate == candidate_rate, "this fixture must keep the headline pass rate identical on both sides"  # => co-07
    print("MATCH: the identical 60% pass rate on both sides would have hidden this exact trade")  # => co-09
    # => co-09: the eval's job is comparing a candidate against a baseline -- the diff, not the raw rate, is the real answer
