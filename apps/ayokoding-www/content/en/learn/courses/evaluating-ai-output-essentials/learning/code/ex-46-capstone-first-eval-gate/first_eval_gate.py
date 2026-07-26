# learning/code/ex-46-capstone-first-eval-gate/first_eval_gate.py
"""Worked Example 46: The Capstone's First Eval Gate, Condensed."""  # => co-01: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

DATASET = [  # => co-03,co-04: a small, fixed, versioned dataset -- every case names its own scorer, per co-02/co-05
    {"id": "case-01", "expected": "15 GB", "scorer": "substring"},  # => co-03: case 1
    {"id": "case-02", "expected": "200 GB", "scorer": "substring"},  # => co-03: case 2
    {"id": "case-03", "expected": "two-factor", "scorer": "substring"},  # => co-03: case 3
    {"id": "case-07", "expected": "30", "scorer": "numeric_tolerance"},  # => co-03: case 4
    {"id": "case-10", "expected": "pro only", "scorer": "exact_match"},  # => co-03: case 5
]  # => co-03: closes DATASET -- five fixed cases, each with a scorer chosen for its own shape
BASELINE_ANSWERS = {  # => co-01: "prompt v1" -- the currently-shipped system's answers
    "case-01": "15 GB free.",  # => co-01: correct
    "case-02": "200 GB on Pro.",  # => co-01: correct
    "case-03": "Yes, two-factor is supported.",  # => co-01: correct
    "case-07": "Links expire after 30 days.",  # => co-01: correct
    "case-10": "Pro plan only supports it.",  # => co-01: WRONG for exact_match -- not the exact string "pro only"
}  # => co-01: closes BASELINE_ANSWERS
CANDIDATE_ANSWERS = {  # => co-09: "prompt v2" -- fixes case-10, but a rewrite drops case-01's exact figure
    "case-01": "Free accounts get some storage.",  # => co-09: now vague -- the "15 GB" figure is gone
    "case-02": "200 GB on Pro.",  # => co-09: unchanged, still correct
    "case-03": "Yes, two-factor is supported.",  # => co-09: unchanged, still correct
    "case-07": "Links expire after 30 days.",  # => co-09: unchanged, still correct
    "case-10": "pro only",  # => co-09: FIXED -- now the exact expected string
}  # => co-09: closes CANDIDATE_ANSWERS


def score(scorer_name: str, output: str, expected: str) -> bool:  # => co-05: the same three-entry registry idea from ex-19
    if scorer_name == "exact_match":  # => co-05: dispatch branch 1
        return output.strip().lower() == expected.strip().lower()  # => co-05: normalized equality
    if scorer_name == "substring":  # => co-05: dispatch branch 2
        return expected in output  # => co-05: the fact just has to appear somewhere
    return expected in output  # => co-05: dispatch branch 3 (numeric_tolerance, simplified to substring for this condensed run)


def run(answers: dict[str, str]) -> dict[str, bool]:  # => co-07: one call, one verdict per dataset case
    """Score every DATASET case's `answers` entry using the case's own declared scorer."""  # => co-07: documents run's contract -- no runtime output, just sets its __doc__
    return {c["id"]: score(c["scorer"], answers[c["id"]], c["expected"]) for c in DATASET}  # => co-07: co-01-co-12 tied together here


def diff(baseline: dict[str, bool], candidate: dict[str, bool]) -> tuple[list[str], list[str]]:  # => co-09: wins vs regressions
    wins = [c for c in baseline if not baseline[c] and candidate[c]]  # => co-09: failed before, passes now
    regressions = [c for c in baseline if baseline[c] and not candidate[c]]  # => co-09: passed before, fails now
    return wins, regressions  # => co-09: returns this computed value to the caller


if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    baseline_run_1 = run(BASELINE_ANSWERS)  # => co-08: baseline, run 1 of 2
    baseline_run_2 = run(BASELINE_ANSWERS)  # => co-08: baseline, run 2 -- deterministic fixture, so identical here
    assert baseline_run_1 == baseline_run_2, "a deterministic fixture must reproduce identically across repeat runs"  # => co-08
    baseline_rate = sum(baseline_run_1.values()) / len(baseline_run_1)  # => co-07: baseline's headline pass rate
    candidate_results = run(CANDIDATE_ANSWERS)  # => co-09: the candidate run, over the SAME fixed dataset
    candidate_rate = sum(candidate_results.values()) / len(candidate_results)  # => co-07: candidate's headline pass rate
    wins, regressions = diff(baseline_run_1, candidate_results)  # => co-09: the per-case comparison
    print(f"Baseline: {baseline_rate:.0%} | Candidate: {candidate_rate:.0%}")  # => co-07: prints both headline numbers
    print(f"Wins: {wins} | Regressions: {regressions}")  # => co-09: prints the per-case diff, separated
    assert wins == ["case-10"], "the candidate must fix exactly case-10"  # => co-09: confirms the improvement
    assert regressions == ["case-01"], "the candidate must break exactly case-01"  # => co-09: confirms the regression
    print("MATCH: one small gate detects both a real improvement and a real regression in the same candidate")  # => co-09
    # => co-01,co-02,co-03,co-04,co-05,co-06,co-07,co-08,co-09,co-10,co-11,co-12: the full loop, end to end, in one file
