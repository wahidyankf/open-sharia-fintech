# learning/code/ex-12-normalized-match/normalized_match.py
"""Worked Example 12: Normalized Match."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def normalize(text: str) -> str:  # => co-05: one shared normalization step both sides of the comparison go through
    """Lowercase and strip leading/trailing whitespace -- removes purely cosmetic differences."""  # => co-05: documents normalize's contract -- no runtime output, just sets its __doc__
    return text.strip().lower()  # => co-05: whitespace and case are the two most common cosmetic diffs


def normalized_match(output: str, expected: str) -> bool:  # => co-05: exact_match, but on normalized text
    """Pass iff `output` and `expected` are identical after normalize()."""  # => co-05: documents normalized_match's contract -- no runtime output, just sets its __doc__
    return normalize(output) == normalize(expected)  # => co-05: both sides normalized -- no asymmetric comparison


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    expected = "pro only"  # => co-04: the same expected answer ex-11 used
    cosmetic_diff = "  Pro Only  "  # => co-05: same content, different case AND stray whitespace
    genuine_diff = "free only"  # => co-05: a REAL content difference -- must still fail after normalization
    cosmetic_result = normalized_match(cosmetic_diff, expected)  # => co-05: the case ex-11's exact_match wrongly failed
    genuine_result = normalized_match(genuine_diff, expected)  # => co-05: a real mismatch, unaffected by normalization
    print(f"normalized_match({cosmetic_diff!r}, {expected!r}) = {cosmetic_result}")  # => co-05: prints the recovered pass
    print(f"normalized_match({genuine_diff!r}, {expected!r}) = {genuine_result}")  # => co-05: prints the still-correct fail
    assert cosmetic_result is True, "a purely cosmetic diff must now pass"  # => co-05: confirms the fix over ex-11
    assert genuine_result is False, "a genuine content difference must still fail"  # => co-05: confirms it isn't now too loose
    print("MATCH: normalization fixes the cosmetic false-fail without hiding a real mismatch")  # => co-05
    # => co-05: normalization trades a small amount of strictness for immunity to whitespace/case noise -- a fair trade here
