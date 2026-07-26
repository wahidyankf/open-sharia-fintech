# learning/code/ex-28-n-of-k-pass-criterion/n_of_k.py
"""Worked Example 28: N-of-K Pass Criterion."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

TRIAL_VERDICTS = {  # => co-08: the same trial-by-trial history ex-27 produced, reused here as a fixture
    "case-01": [True, True, True, True, True],  # => co-08: 5/5 -- rock solid
    "case-08": [True, True, False, False, False],  # => co-08: 2/5 -- the flaky case
    "case-12": [True, True, True, True, True],  # => co-08: 5/5 -- rock solid
}


def passes_n_of_k(verdicts: list[bool], *, k: int) -> bool:  # => co-07: a case counts as passing only above a threshold
    """Pass iff at least `k` of `verdicts` are True."""  # => co-07: documents passes_n_of_k's contract -- no runtime output, just sets its __doc__
    return sum(verdicts) >= k  # => co-07: a strict count, not a majority-of-half rule


if __name__ == "__main__":  # => co-08: entry point -- runs only when this file executes directly, not on import
    threshold_k = 4  # => co-02: a WRITTEN decision -- require at least 4 of 5 trials to pass, not just "most"
    print(f"Requiring at least {threshold_k} of 5 trials to pass")  # => co-02: states the threshold up front
    case_verdicts: dict[str, bool] = {}  # => co-08: one final n-of-k verdict per case
    for case_id, trials in TRIAL_VERDICTS.items():  # => co-08: apply the SAME threshold to every case, uniformly
        final_verdict = passes_n_of_k(trials, k=threshold_k)  # => co-07: reduce 5 trial results to one final verdict
        case_verdicts[case_id] = final_verdict  # => co-08: record this case's final, threshold-applied verdict
        print(f"  {case_id}: {sum(trials)}/5 passed -> final verdict {final_verdict}")  # => co-08: prints the reduction
    assert case_verdicts["case-01"] is True, "5/5 must clear a 4-of-5 threshold"  # => co-08: confirms the solid case
    assert case_verdicts["case-08"] is False, "2/5 must NOT clear a 4-of-5 threshold"  # => co-08: confirms the flaky case fails
    assert case_verdicts["case-12"] is True, "5/5 must clear a 4-of-5 threshold"  # => co-08: confirms the other solid case
    print("MATCH: the flaky case is correctly failed, without needing a single perfectly-stable trial")  # => co-08
    # => co-08: n-of-k turns "sometimes right" into an honest fail, instead of averaging it into a comfortable pass rate
