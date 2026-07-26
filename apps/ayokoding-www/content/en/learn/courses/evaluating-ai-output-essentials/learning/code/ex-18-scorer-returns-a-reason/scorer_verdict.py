# learning/code/ex-18-scorer-returns-a-reason/scorer_verdict.py
"""Worked Example 18: A Scorer Returns a Reason."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import NamedTuple  # => co-05: a typed record beats a bare bool for a debuggable scorer result


class Verdict(NamedTuple):  # => co-05: EVERY scorer in this topic returns this shape from here on
    passed: bool  # => co-05: the pass/fail decision itself
    reason: str  # => co-05: WHY -- what a human reads instead of re-deriving it from the raw output


def substring_scorer_with_reason(output: str, required_fact: str) -> Verdict:  # => co-05: ex-13's scorer, upgraded
    """Pass iff `required_fact` appears in `output`; the reason names the exact fact checked."""  # => co-05: documents substring_scorer_with_reason's contract -- no runtime output, just sets its __doc__
    found = required_fact in output  # => co-05: the same check as ex-13, unchanged
    if found:  # => co-05: branch the reason text on the outcome, not just the boolean
        return Verdict(passed=True, reason=f"found required fact {required_fact!r}")  # => co-05: a reason confirming success
    return Verdict(passed=False, reason=f"missing required fact {required_fact!r}")  # => co-05: a reason naming the exact gap


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    required_fact = "15 GB"  # => co-04: case-01's required fact, reused from ex-13
    answer = "New Nimbus accounts start with a generous amount of free storage."  # => co-05: deliberately missing the fact
    verdict = substring_scorer_with_reason(answer, required_fact)  # => co-05: one call, one self-explaining result
    print(f"passed={verdict.passed}, reason={verdict.reason!r}")  # => co-05: prints both fields -- no re-running needed to know why
    assert verdict.passed is False, "this answer must fail -- it never states the required fact"  # => co-05: confirms the fail path
    assert verdict.reason == "missing required fact '15 GB'", "the reason must name the exact missing fact"  # => co-05
    print("MATCH: a failing verdict now explains itself without re-reading the scorer's source")  # => co-05
    # => co-05: a bare True/False forces someone to re-derive WHY on every failure -- a reason answers it once, at scoring time
