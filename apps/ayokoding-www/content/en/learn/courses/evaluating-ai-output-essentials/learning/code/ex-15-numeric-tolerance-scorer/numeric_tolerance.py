# learning/code/ex-15-numeric-tolerance-scorer/numeric_tolerance.py
"""Worked Example 15: Numeric-Tolerance Scorer."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import re  # => co-05: pulls the first number out of a free-text answer before comparing it

NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")  # => co-05: matches an integer or decimal, optionally negative


def numeric_tolerance_scorer(output: str, expected: float, *, tolerance: float) -> bool:  # => co-05: for numbers, not exact text
    """Pass iff the first number found in `output` is within `tolerance` of `expected`."""  # => co-05: documents numeric_tolerance_scorer's contract -- no runtime output, just sets its __doc__
    match = NUMBER_PATTERN.search(output)  # => co-05: locate the first numeric token in the free-text answer
    if match is None:  # => co-05: no number at all -- cannot possibly satisfy a numeric criterion
        return False  # => co-05: fail closed rather than raising on a malformed answer
    found_value = float(match.group())  # => co-05: parse the matched substring into an actual float
    return abs(found_value - expected) <= tolerance  # => co-05: within tolerance, inclusive of the boundary itself


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    expected = 30.0  # => co-04: case-07's expected share-link-expiry value, in days
    exact_answer = "Nimbus share links expire after 30 days by default."  # => co-05: matches expected exactly
    close_answer = "Nimbus share links expire after roughly 31 days by default."  # => co-05: one day off -- close, arguably fine
    far_answer = "Nimbus share links expire after 90 days by default."  # => co-05: far off -- a genuine wrong answer
    exact_result = numeric_tolerance_scorer(exact_answer, expected, tolerance=1.0)  # => co-05: within tolerance, at 0 distance
    close_result = numeric_tolerance_scorer(close_answer, expected, tolerance=1.0)  # => co-05: exactly on the tolerance boundary
    far_result = numeric_tolerance_scorer(far_answer, expected, tolerance=1.0)  # => co-05: well outside the tolerance
    print(f"exact (30, tol=1.0) = {exact_result}")  # => co-05: prints the exact-match case's verdict
    print(f"close (31, tol=1.0) = {close_result}")  # => co-05: prints the boundary case's verdict
    print(f"far (90, tol=1.0) = {far_result}")  # => co-05: prints the far-off case's verdict
    assert exact_result is True, "an exact numeric match must pass"  # => co-05: confirms the zero-distance case
    assert close_result is True, "a value exactly at the tolerance boundary must still pass (inclusive)"  # => co-05
    assert far_result is False, "a value well outside the tolerance must fail"  # => co-05: confirms the fail path
    print("MATCH: tolerance absorbs harmless numeric noise without accepting a genuinely wrong number")  # => co-05
    # => co-05: the tolerance itself is a written decision (co-02) -- too wide hides real drift, too narrow flags rounding noise
