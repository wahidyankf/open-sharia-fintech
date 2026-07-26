# learning/code/ex-41-model-swap-under-the-same-eval/model_swap.py
"""Worked Example 41: Model Swap Under the Same Eval."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

FIXED_CASES = {"case-01": "15 GB", "case-02": "200 GB", "case-08": "24-hour"}  # => co-03: the SAME three cases, unchanged
BACKEND_A_ANSWERS = {  # => co-09: "model backend A" -- answers as they existed before the swap
    "case-01": "Free accounts get 15 GB.",  # => co-09: correct
    "case-02": "Pro includes 200 GB.",  # => co-09: correct
    "case-08": "Free support targets 24-hour response.",  # => co-09: correct
}  # => co-09: closes BACKEND_A_ANSWERS -- all three correct
BACKEND_B_ANSWERS = {  # => co-09: "model backend B" -- a DIFFERENT underlying model, same eval, same cases
    "case-01": "Free accounts get 15 GB.",  # => co-09: unchanged, still correct
    "case-02": "Pro includes 200 GB.",  # => co-09: unchanged, still correct
    "case-08": "Free support targets same-day response.",  # => co-09: rephrased -- dropped the exact figure
}  # => co-09: closes BACKEND_B_ANSWERS -- case-08 now phrased differently, dropping the exact figure


def run_eval(answers: dict[str, str]) -> dict[str, bool]:  # => co-09: the SAME eval logic, applied to WHATEVER backend answered
    """Score each fixed case's answer for the required fact -- the eval itself never changes."""  # => co-09: documents run_eval's contract -- no runtime output, just sets its __doc__
    return {cid: FIXED_CASES[cid] in answers[cid] for cid in FIXED_CASES}  # => co-05: substring scoring, unchanged from Theme B


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    results_a = run_eval(BACKEND_A_ANSWERS)  # => co-09: run the UNCHANGED eval against backend A
    results_b = run_eval(BACKEND_B_ANSWERS)  # => co-09: run the SAME UNCHANGED eval against backend B
    rate_a = sum(results_a.values()) / len(results_a)  # => co-07: backend A's headline number
    rate_b = sum(results_b.values()) / len(results_b)  # => co-07: backend B's headline number
    print(f"Backend A: {results_a} -> {rate_a:.0%}")  # => co-09: prints backend A's per-case results and rate
    print(f"Backend B: {results_b} -> {rate_b:.0%}")  # => co-09: prints backend B's per-case results and rate
    assert rate_a == 1.0, "backend A must pass every case in this fixture"  # => co-07: confirms backend A's baseline
    assert rate_b < rate_a, "swapping the backend must be detectable purely from the pass rate dropping"  # => co-09
    print("MATCH: the eval code did not change at all -- only which backend answered the fixed cases changed")  # => co-09
    # => co-09: the SAME dataset and scorers work unmodified across a model swap -- that portability is exactly the point
