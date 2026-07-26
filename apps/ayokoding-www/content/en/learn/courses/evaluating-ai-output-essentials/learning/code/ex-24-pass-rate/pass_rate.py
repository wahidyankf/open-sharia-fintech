# learning/code/ex-24-pass-rate/pass_rate.py
"""Worked Example 24: Pass Rate."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def pass_rate(verdicts: list[bool]) -> float:  # => co-07: reduces N booleans to ONE comparable number
    """Return the fraction of True verdicts in `verdicts`; 0.0 for an empty list."""  # => co-07: documents pass_rate's contract -- no runtime output, just sets its __doc__
    if not verdicts:  # => co-07: an empty run has no cases to divide by -- define it as 0.0, not a crash
        return 0.0  # => co-07: fail-safe default rather than a ZeroDivisionError
    return sum(verdicts) / len(verdicts)  # => co-07: True counts as 1, False as 0 -- sum() IS the pass count


if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    all_pass = [True, True, True, True]  # => co-07: a perfect run
    mixed = [True, True, False, True, False]  # => co-07: three passes, two fails -- the common case
    empty: list[bool] = []  # => co-07: the degenerate, zero-case run
    all_pass_rate = pass_rate(all_pass)  # => co-07: 4/4
    mixed_rate = pass_rate(mixed)  # => co-07: 3/5
    empty_rate = pass_rate(empty)  # => co-07: defined as 0.0, never a crash
    print(f"all_pass -> {all_pass_rate:.2%}")  # => co-07: prints the perfect-run rate
    print(f"mixed -> {mixed_rate:.2%}")  # => co-07: prints the common-case rate
    print(f"empty -> {empty_rate:.2%}")  # => co-07: prints the degenerate-case rate
    assert all_pass_rate == 1.0, "a perfect run must reduce to exactly 1.0"  # => co-07: confirms the ceiling
    assert mixed_rate == 0.6, "three passes out of five must reduce to exactly 0.6"  # => co-07: confirms the arithmetic
    assert empty_rate == 0.0, "an empty run must reduce to 0.0, never raise"  # => co-07: confirms the edge case
    print("MATCH: one number, reproducibly computed, is what actually gets compared across runs")  # => co-07
    # => co-07: a wall of per-case output tells you WHAT changed; the pass rate is what tells you IF it got better
