# learning/code/ex-01-the-vibe-check-fails/vibe_check.py
"""Worked Example 1: The Vibe Check Fails."""  # => co-01: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

CASE_A = "Nimbus gives every account 15 GB of free storage."  # => co-01: the ONE case the engineer actually tried by hand
CASE_A_KEY_FACT = "15 GB"  # => co-01: the fact a correct answer to Case A must keep

CASE_B = "Nimbus accounts start on the Free plan, and upgrading unlocks 200 GB of storage."  # => co-01: a SECOND, never-tried case
CASE_B_KEY_FACT = "200 GB"  # => co-01: the fact a correct answer to Case B must keep


def answer_v1(question_context: str) -> str:  # => co-01: stands in for "our LLM-backed FAQ answerer, prompt-tuned by hand"
    """Return everything up to the first comma -- a heuristic hand-tuned only against CASE_A."""  # => co-01: documents answer_v1's contract -- no runtime output, just sets its __doc__
    comma_index = question_context.find(",")  # => co-01: locate the first comma, if any
    if comma_index == -1:  # => co-01: CASE_A has no comma -- this branch is the ONLY one the engineer ever exercised
        return question_context  # => co-01: unmodified text -- looks perfect on the one case tried
    return question_context[:comma_index] + "."  # => co-01: truncate at the comma -- silently drops everything after it


if __name__ == "__main__":  # => co-01: entry point -- runs only when this file executes directly, not on import
    result_a = answer_v1(CASE_A)  # => co-01: the tuning pass -- run against the one case the engineer had in mind
    print(f"Case A -> {result_a!r}")  # => co-01: prints the tuned result
    case_a_ok = CASE_A_KEY_FACT in result_a  # => co-01: does the key fact survive?
    print(f"Case A keeps {CASE_A_KEY_FACT!r}: {case_a_ok}")  # => co-01: True -- ships with confidence
    assert case_a_ok, "Case A must look correct by hand -- that's the whole trap"  # => co-01: confirms the false confidence

    result_b = answer_v1(CASE_B)  # => co-01: the SAME prompt, run against a case never eyeballed
    print(f"Case B -> {result_b!r}")  # => co-01: prints the tuned result on the untried case
    case_b_ok = CASE_B_KEY_FACT in result_b  # => co-01: does the key fact survive this time?
    print(f"Case B keeps {CASE_B_KEY_FACT!r}: {case_b_ok}")  # => co-01: False -- the regression a vibe check cannot see
    assert not case_b_ok, "Case B's key fact must be silently dropped -- that's the regression"  # => co-01: proves it
    print("MATCH: hand-tuning on one case hid a real regression on a second case")  # => co-01: reached only if both asserts passed
    # => co-01: this script is self-verifying -- a clean exit means the demonstrated claim held for these two cases
