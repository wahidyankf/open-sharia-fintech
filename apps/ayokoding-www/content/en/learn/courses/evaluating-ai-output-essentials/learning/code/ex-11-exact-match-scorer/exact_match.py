# learning/code/ex-11-exact-match-scorer/exact_match.py
"""Worked Example 11: Exact-Match Scorer."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def exact_match(output: str, expected: str) -> bool:  # => co-05: the cheapest scorer that exists -- string equality
    """Pass iff `output` is character-for-character identical to `expected`."""  # => co-04: documents exact_match's contract -- no runtime output, just sets its __doc__
    return output == expected  # => co-05: no normalization, no tolerance -- byte-identical or fail


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    expected = "pro only"  # => co-04: case-10's exact expected answer, from the co-03 dataset
    passing_output = "pro only"  # => co-05: a candidate that matches character-for-character
    failing_output = "Pro Only"  # => co-05: a candidate that differs ONLY in letter case
    pass_result = exact_match(passing_output, expected)  # => co-05: the pass path
    fail_result = exact_match(failing_output, expected)  # => co-05: the fail path -- even a trivial casing difference fails
    print(f"exact_match({passing_output!r}, {expected!r}) = {pass_result}")  # => co-05: prints the pass verdict
    print(f"exact_match({failing_output!r}, {expected!r}) = {fail_result}")  # => co-05: prints the fail verdict
    assert pass_result is True, "an identical string must pass exact_match"  # => co-05: confirms the pass path
    assert fail_result is False, "even a one-letter casing difference must fail exact_match"  # => co-05: confirms the fail path
    print("MATCH: exact_match costs nothing to run and never drifts -- but is brittle to any cosmetic difference")  # => co-05
    # => co-05: exact_match is correct for single-answer cases -- ex-12 fixes its brittleness to cosmetic differences
