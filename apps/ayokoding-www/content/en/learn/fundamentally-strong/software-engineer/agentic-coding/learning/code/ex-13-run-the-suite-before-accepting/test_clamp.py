# learning/code/ex-13-run-the-suite-before-accepting/test_clamp.py
"""Example ex-13: Run the Suite Before Accepting -- pytest-style tests for clamp()."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

# NAMING TRAP: despite the test_*.py / test_* naming, this file does NOT run under pytest      # => co-13: flags the exact confusion this file's own name invites
# directly -- `pytest test_clamp.py` errors ("fixture 'clamp_fn' not found") because            # => co-13: clamp_fn is a required positional parameter, not a fixture pytest can supply
# test_clamp() takes a required clamp_fn argument. Run this file via `python3 test_clamp.py`.   # => co-13: the correct, documented path -- see this page's Run: line

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-13: types the clamp_fn parameter test_clamp/run_suite are quantified over

from clamp import clamp_v1, clamp_v2  # => co-13: imports BOTH candidate diffs from the colocated clamp.py -- no hidden dependency


def test_clamp(clamp_fn: Callable[[float, float, float], float]) -> None:  # => co-13: pytest-style test function -- named test_*, plain asserts, runnable by hand with no framework installed
    """The suite: below-range, in-range, and above-range values must all clamp correctly."""  # => co-13: documents the test's contract
    assert clamp_fn(-5, 0, 10) == 0, "value below low must clamp UP to low"  # => co-13: the exact case clamp_v1 fails
    assert clamp_fn(5, 0, 10) == 5, "value already in range must pass through unchanged"  # => co-13: sanity case both versions pass
    assert clamp_fn(15, 0, 10) == 10, "value above high must clamp DOWN to high"  # => co-13: sanity case both versions pass


def run_suite(name: str, clamp_fn: Callable[[float, float, float], float]) -> bool:  # => co-13: a tiny hand-rolled runner -- catches the AssertionError a real pytest run would report
    """Run test_clamp against `clamp_fn`; return True on pass, False on the first failure."""  # => co-13: documents run_suite's contract
    try:  # => co-13: a real test run either raises AssertionError (fail) or returns cleanly (pass)
        test_clamp(clamp_fn)  # => co-13: runs the suite above against this specific candidate function
    except AssertionError as exc:  # => co-13: pytest reports exactly this exception type on a failed assert
        print(f"{name}: FAIL -- {exc}")  # => co-13: the rejection reason, logged BEFORE any acceptance decision
        return False  # => co-13: signals rejection to the caller
    print(f"{name}: PASS -- all three boundary cases hold")  # => co-13: only reached if every assert above passed
    return True  # => co-13: signals acceptance to the caller


if __name__ == "__main__":  # => co-13: entry point -- this block runs only when the file executes directly, not on import
    print("--- Running suite against the agent's FIRST diff (clamp_v1) ---")  # => co-13: labels which diff is under test
    first_diff_accepted = run_suite("clamp_v1", clamp_v1)  # => co-13: THIS call is the "run the suite before accepting" gate
    assert first_diff_accepted is False, "clamp_v1 must fail: it never clamps values below low"  # => co-13: confirms the rejection was correct
    print("--- clamp_v1 REJECTED: failing test blocks acceptance ---")  # => co-13: the rejection is explicit, not silent
    print()  # => co-13: blank line, purely for transcript readability
    print("--- Running suite against the agent's SECOND diff (clamp_v2, the fix) ---")  # => co-13: labels the retry
    second_diff_accepted = run_suite("clamp_v2", clamp_v2)  # => co-13: same gate, now against the fixed candidate
    assert second_diff_accepted is True, "clamp_v2 must pass: it clamps both bounds"  # => co-13: confirms acceptance was correct
    print("--- clamp_v2 ACCEPTED: suite passes, diff is safe to build on ---")  # => co-13: reached only if both asserts above passed
