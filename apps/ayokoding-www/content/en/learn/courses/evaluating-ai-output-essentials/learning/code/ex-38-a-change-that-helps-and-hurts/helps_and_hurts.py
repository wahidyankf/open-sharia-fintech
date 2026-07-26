# learning/code/ex-38-a-change-that-helps-and-hurts/helps_and_hurts.py
"""Worked Example 38: A Change That Helps AND Hurts."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

BASELINE = {  # => co-01: "prompt v1" -- three known failures: case-06, case-08, case-11
    "case-01": True,  # => co-01: pass
    "case-02": True,  # => co-01: pass
    "case-03": True,  # => co-01: pass
    "case-04": True,  # => co-01: pass
    "case-05": True,  # => co-01: pass
    "case-06": False,  # => co-01: cases 1-6
    "case-07": True,  # => co-01: pass
    "case-08": False,  # => co-01: known failure
    "case-09": True,  # => co-01: pass
    "case-10": True,  # => co-01: pass
    "case-11": False,  # => co-01: known failure
    "case-12": True,  # => co-01: cases 7-12
}  # => co-01: closes BASELINE -- nine pass, three fail -> 75%
CANDIDATE = {  # => co-09: "prompt v2" -- a rewrite aimed squarely at fixing case-06, case-08, and case-11
    "case-01": False,  # => co-09: NOW BROKEN
    "case-02": True,  # => co-09: pass
    "case-03": True,  # => co-09: pass
    "case-04": True,  # => co-09: pass
    "case-05": True,  # => co-09: pass
    "case-06": True,  # => co-09: case-01 NOW BROKEN
    "case-07": True,  # => co-09: pass
    "case-08": True,  # => co-09: now fixed
    "case-09": True,  # => co-09: pass
    "case-10": True,  # => co-09: pass
    "case-11": True,  # => co-09: now fixed
    "case-12": False,  # => co-09: case-12 NOW BROKEN
}  # => co-09: closes CANDIDATE -- ten pass, two fail -> 83%, and it fixed all three targeted cases


def diff_runs(baseline: dict[str, bool], candidate: dict[str, bool]) -> tuple[list[str], list[str]]:  # => co-09: same shape as ex-37
    """Return (wins, regressions) between `baseline` and `candidate`."""  # => co-09: documents diff_runs's contract -- no runtime output, just sets its __doc__
    wins = [cid for cid in baseline if not baseline[cid] and candidate[cid]]  # => co-09: failed before, passes now
    regressions = [cid for cid in baseline if baseline[cid] and not candidate[cid]]  # => co-09: passed before, fails now
    return wins, regressions  # => co-09: returns this computed value to the caller


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    baseline_rate = sum(BASELINE.values()) / len(BASELINE)  # => co-07: the baseline's headline number
    candidate_rate = sum(CANDIDATE.values()) / len(CANDIDATE)  # => co-07: the candidate's headline number
    wins, regressions = diff_runs(BASELINE, CANDIDATE)  # => co-09: the per-case diff -- what the headline number alone hides
    print(f"Baseline: {baseline_rate:.0%} | Candidate: {candidate_rate:.0%}")  # => co-07: the pass rate LOOKS like a clean win
    print(f"Wins: {sorted(wins)}")  # => co-09: three cases genuinely fixed
    print(f"Regressions: {sorted(regressions)}")  # => co-09: two cases the rewrite quietly broke
    assert candidate_rate > baseline_rate, "the net pass rate must go UP -- that's exactly what makes this trap dangerous"  # => co-07
    assert sorted(wins) == ["case-06", "case-08", "case-11"], "exactly the three targeted cases must be fixed"  # => co-09
    assert sorted(regressions) == ["case-01", "case-12"], "exactly two previously-solid cases must be newly broken"  # => co-09
    print("MATCH: the pass rate alone says 'ship it' -- only the per-case diff shows what it would break")  # => co-09
    # => co-09: 'quality improved' and 'quality improved everywhere' are different claims -- only the per-case diff proves either
