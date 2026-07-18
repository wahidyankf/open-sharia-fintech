# learning/code/ex-20-coverage-number-without-assertions/test_discount_weak.py
"""ex-20: a test that reaches 100% line coverage of discount.py, and asserts NOTHING real (co-12)."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from discount import apply_discount  # => co-12: imports the ONE function this whole test file exercises


def test_apply_discount_runs() -> None:  # => co-12: pytest collects this because its name starts with test_
    """Call apply_discount -- covers its one line -- but check nothing about the RESULT."""  # => co-12: documents this test's own (weak) contract
    result = apply_discount(100.0, 0.2)  # => co-12: this call is what makes coverage report 100% -- the line RUNS
    assert result is not None  # => co-12: an assertion that is ALWAYS true for a float return -- verifies NOTHING
    # => co-12: this test passes for ANY numeric return value -- $20, $80, or -$500 all satisfy "is not None"
