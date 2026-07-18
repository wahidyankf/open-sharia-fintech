# learning/code/ex-47-reject-a-confidently-wrong-refactor/reject_wrong_refactor.py
"""Example ex-47: Reject a Confidently Wrong Refactor -- Off-By-One Caught by Regression Test."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-16: types the fn parameter test_sum_even_up_to/run_regression are quantified over


def sum_even_up_to_original(limit: int) -> int:  # => co-16: the ORIGINAL, correct implementation -- what the agent was asked to "simplify"
    """Sum every even number from 0 through `limit`, inclusive."""  # => co-16: documents the contract BOTH versions claim to implement
    total = 0  # => co-16: running total, starts at zero
    n = 0  # => co-16: loop counter, starts at zero
    while n <= limit:  # => co-16: inclusive of `limit` itself -- the detail the refactor drops
        if n % 2 == 0:  # => co-16: only even numbers count toward the sum
            total += n  # => co-16: accumulates this even number
        n += 1  # => co-16: advances the counter by one
    return total  # => co-16: the correct, inclusive sum


def sum_even_up_to_refactored(limit: int) -> int:  # => co-16: THE AGENT'S "SIMPLIFICATION" -- confidently wrong, changes behavior silently
    """Sum every even number from 0 through `limit` (refactored -- silently EXCLUDES `limit` itself)."""  # => co-16: documents the (wrong) contract this diff actually implements
    return sum(n for n in range(0, limit) if n % 2 == 0)  # => co-16: BUG -- range(0, limit) is exclusive of `limit`, dropping it when `limit` is even


def test_sum_even_up_to(fn: Callable[[int], int]) -> None:  # => co-13: the REGRESSION TEST -- written against the original's documented, inclusive contract
    """Regression test: sum of even numbers from 0 through 10, inclusive, must be 30."""  # => co-13: documents the test's contract
    assert fn(10) == 30, f"expected 30 (0+2+4+6+8+10), got {fn(10)}"  # => co-13: 10 is even -- exactly the case the refactor's off-by-one drops


def run_regression(name: str, fn: Callable[[int], int]) -> bool:  # => co-13: a tiny hand-rolled runner -- catches the AssertionError a real pytest run would report
    """Run test_sum_even_up_to against `fn`; return True on pass, False on the first failure."""  # => co-13: documents run_regression's contract
    try:  # => co-13: a real test run either raises AssertionError (fail) or returns cleanly (pass)
        test_sum_even_up_to(fn)  # => co-13: runs the regression test above against this specific candidate
    except AssertionError as exc:  # => co-13: pytest reports exactly this exception type on a failed assert
        print(f"{name}: FAIL -- {exc}")  # => co-13: the rejection reason, logged BEFORE any acceptance decision
        return False  # => co-13: signals rejection to the caller
    print(f"{name}: PASS")  # => co-13: only reached if the assert above passed
    return True  # => co-13: signals acceptance to the caller


if __name__ == "__main__":  # => co-16: entry point -- this block runs only when the file executes directly, not on import
    print("--- Running regression test against the ORIGINAL implementation ---")  # => co-16: labels which version is under test
    original_ok = run_regression("sum_even_up_to_original", sum_even_up_to_original)  # => co-16: confirms the baseline the refactor must preserve
    assert original_ok is True, "the original implementation must pass its own regression test"  # => co-16: sanity check on the baseline itself
    print()  # => co-16: blank line, purely for transcript readability
    print("--- Running the SAME regression test against the REFACTORED implementation ---")  # => co-16: labels the refactor under test
    refactored_ok = run_regression("sum_even_up_to_refactored", sum_even_up_to_refactored)  # => co-16: THIS is where the silent behavior change gets caught
    assert refactored_ok is False, "the refactored version must FAIL: it silently drops `limit` when limit is even"  # => co-16: confirms the catch was correct
    print("--- REFACTOR REJECTED: regression test caught a silent behavior change ---")  # => co-16: the rejection is explicit, not silent
    print("Rejection reason: range(0, limit) excludes limit itself -- must be range(0, limit + 1).")  # => co-16: documented reason, not a vague "looks wrong"
