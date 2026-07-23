# learning/code/ex-27-failing-test-tripwire/tripwire_demo.py
"""Example 27: Failing Test as a Tripwire (Red-to-Green Transition)."""  # => co-14: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-14: types the count_positive parameter tripwire_test is quantified over


def count_positive_v1(numbers: list[int]) -> int:  # => co-14: the agent's FIRST attempt -- written before seeing the failure
    """First agent attempt: counts non-negative numbers (BUG: treats 0 as positive)."""  # => co-14: documents count_positive_v1's contract -- no runtime output, just sets its __doc__
    return sum(1 for n in numbers if n >= 0)  # => co-14: BUG -- >= 0 includes zero, which is not "positive"


def count_positive_v2(numbers: list[int]) -> int:  # => co-14: the fix, applied only AFTER the red run below
    """Fixed implementation: counts strictly-positive numbers only."""  # => co-14: documents count_positive_v2's contract -- no runtime output, just sets its __doc__
    return sum(1 for n in numbers if n > 0)  # => co-14: > 0 correctly excludes zero


def tripwire_test(count_positive: Callable[[list[int]], int]) -> None:  # => co-14: the acceptance bar, written BEFORE any fix exists
    """The acceptance-bar test written BEFORE the fix -- forbids 'done' until this passes."""  # => co-14: documents tripwire_test's contract -- no runtime output, just sets its __doc__
    numbers = [1, 2, 0, -3, 4]  # => co-14: chosen so the zero-vs-strictly-positive bug is directly observable
    expected = 3  # => co-14: only 1, 2, 4 are strictly positive -- 0 and -3 are excluded
    actual = count_positive(numbers)  # => co-14: runs whichever implementation is passed in
    assert actual == expected, f"expected {expected}, got {actual}"  # => co-14: this IS the tripwire -- it forbids claiming "done" while False


if __name__ == "__main__":  # => co-14: entry point -- this block runs only when the file executes directly, not on import
    print("--- RED: running tripwire test against the first (buggy) attempt ---")  # => co-14: labels the RED phase
    try:  # => co-14: the buggy v1 implementation is EXPECTED to fail this test
        tripwire_test(count_positive_v1)  # => co-14: runs the acceptance bar against the first attempt
        red_failed = False  # => co-14: reached only if the buggy implementation unexpectedly passed
    except AssertionError as exc:  # => co-14: the expected outcome -- the tripwire fired
        red_failed = True  # => co-14: records that the test genuinely failed, not just that code ran
        print(f"FAILED (as expected): {exc}")  # => co-14: the captured failure message, logged as a rejection reason
    assert red_failed, "the tripwire test MUST fail against the buggy v1 implementation"  # => co-14: verifies the RED phase was genuine
    print("Verdict: RED -- completion claim is BLOCKED\n")  # => co-14: no "done" claim is allowed while red

    print("--- GREEN: running tripwire test against the fixed attempt ---")  # => co-14: labels the GREEN phase
    tripwire_test(count_positive_v2)  # => co-14: no exception here means the fix satisfies the SAME test unchanged
    print("PASSED")  # => co-14: reached only if the fixed implementation passed
    print("Verdict: GREEN -- completion claim is now ALLOWED\n")  # => co-14: the tripwire has cleared

    print("Red-to-green transition observed: True")  # => co-14: this file is self-verifying -- a clean exit proves both phases ran as claimed
