# learning/capstone/code/compare.py
"""Capstone step 4: diff candidate vs. baseline and accept/reject on regressions, never on pass rate alone (exercises co-07, co-09)."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-09: the artefact format needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-09: locates results_baseline.json relative to this script

BASELINE_PATH = Path(__file__).parent / "results_baseline.json"  # => co-09: the artefact runner.py already committed

CANDIDATE_GOOD_VERDICTS = {  # => co-09: "prompt v2" -- fixes BOTH known problems, breaks nothing
    "case-01": True,  # => co-09: pass
    "case-02": True,  # => co-09: pass
    "case-03": True,  # => co-09: pass
    "case-04": True,  # => co-09: pass
    "case-05": True,  # => co-09: pass
    "case-06": True,  # => co-09: 1-6
    "case-07": True,  # => co-09: pass
    "case-08": True,  # => co-09: pass
    "case-09": True,  # => co-09: pass
    "case-10": True,  # => co-09: pass
    "case-11": True,  # => co-09: pass
    "case-12": True,  # => co-09: 7-12
    "case-13": True,  # => co-09: fixed
    "case-14": True,  # => co-09: 13-14 -- both fixed, zero regressions
}  # => co-09: closes CANDIDATE_GOOD_VERDICTS -- 14/14, a genuinely clean win
CANDIDATE_BAD_VERDICTS = {  # => co-09: "prompt v3" -- fixes the SAME two problems, but breaks case-01
    "case-01": False,  # => co-09: NOW BROKEN
    "case-02": True,  # => co-09: pass
    "case-03": True,  # => co-09: pass
    "case-04": True,  # => co-09: pass
    "case-05": True,  # => co-09: pass
    "case-06": True,  # => co-09: case-01 NOW BROKEN
    "case-07": True,  # => co-09: pass
    "case-08": True,  # => co-09: pass
    "case-09": True,  # => co-09: pass
    "case-10": True,  # => co-09: pass
    "case-11": True,  # => co-09: pass
    "case-12": True,  # => co-09: 7-12 unchanged
    "case-13": True,  # => co-09: fixed
    "case-14": True,  # => co-09: 13-14 -- both fixed, LIKE candidate v2
}  # => co-09: closes CANDIDATE_BAD_VERDICTS -- 13/14, a HIGHER pass rate than baseline, hiding a real regression


def diff_runs(baseline: dict[str, bool], candidate: dict[str, bool]) -> tuple[list[str], list[str]]:  # => co-09: wins, regressions
    """Return (wins, regressions) -- case ids that flipped False->True, and True->False, respectively."""  # => co-09: documents diff_runs's contract -- no runtime output, just sets its __doc__
    wins = sorted(cid for cid in baseline if not baseline[cid] and candidate[cid])  # => co-09: failed before, passes now
    regressions = sorted(cid for cid in baseline if baseline[cid] and not candidate[cid])  # => co-09: passed before, fails now
    return wins, regressions  # => co-09: returns this computed value to the caller


def accept_or_reject(baseline: dict[str, bool], candidate: dict[str, bool]) -> tuple[bool, str]:  # => co-09: the real decision
    """Reject if ANY regression exists, regardless of the raw pass-rate delta; accept otherwise."""  # => co-09: documents accept_or_reject's contract -- no runtime output, just sets its __doc__
    wins, regressions = diff_runs(baseline, candidate)  # => co-09: the per-case diff drives this decision, not the headline rate
    if regressions:  # => co-09: a single regression is disqualifying, no matter how many wins accompany it
        return False, f"REJECT -- {len(regressions)} regression(s): {regressions}"  # => co-09: a reason naming the exact cases
    return True, f"ACCEPT -- {len(wins)} win(s), 0 regressions"  # => co-09: a reason naming the exact win count


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    baseline_data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))  # => co-09: load the committed baseline artefact
    baseline_verdicts = baseline_data["verdicts"]  # => co-09: this run's per-case True/False verdicts
    baseline_rate = baseline_data["pass_rate"]  # => co-07: the baseline's own committed headline number

    good_rate = sum(CANDIDATE_GOOD_VERDICTS.values()) / len(CANDIDATE_GOOD_VERDICTS)  # => co-07: candidate v2's headline number
    good_decision, good_reason = accept_or_reject(baseline_verdicts, CANDIDATE_GOOD_VERDICTS)  # => co-09: the real decision
    print(f"Candidate v2: {good_rate:.2%} (baseline {baseline_rate:.2%}) -> {good_reason}")  # => co-09: prints v2's verdict
    assert good_decision is True, "a candidate with zero regressions must be accepted"  # => co-09: confirms the accept path

    bad_rate = sum(CANDIDATE_BAD_VERDICTS.values()) / len(CANDIDATE_BAD_VERDICTS)  # => co-07: candidate v3's headline number
    bad_decision, bad_reason = accept_or_reject(baseline_verdicts, CANDIDATE_BAD_VERDICTS)  # => co-09: the real decision
    print(f"Candidate v3: {bad_rate:.2%} (baseline {baseline_rate:.2%}) -> {bad_reason}")  # => co-09: prints v3's verdict
    assert bad_rate > baseline_rate, "candidate v3 must have a HIGHER raw pass rate than the baseline"  # => co-07: the trap
    assert bad_decision is False, "candidate v3 must be REJECTED despite its higher raw pass rate"  # => co-09: the real check
    print("MATCH: v2 is accepted, v3 is rejected -- even though v3's pass rate alone looks better than the baseline")  # => co-09
    # => co-09: this is the entire point of comparing per-case, not just headline-to-headline -- a rate can lie, a diff cannot
