# learning/code/ex-05-float-rounding-error/float_rounding.py
"""Example 5: 0.1 + 0.2 != 0.3 -- IEEE-754 Rounding Is Structural."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic
from decimal import Decimal  # => co-03: used only to print the EXACT stored binary value, not for math


if __name__ == "__main__":  # => co-03: entry point -- this block runs only when the file executes directly, not on import
    a, b, c = 0.1, 0.2, 0.3  # => co-03: three ordinary Python floats, IEEE-754 binary64 under the hood
    total = a + b  # => co-03: neither 0.1 nor 0.2 has an EXACT binary64 representation -- both already round
    print(f"0.1 + 0.2 = {total!r}")  # => co-03: !r forces Python's shortest-round-trip repr, not a rounded display
    print(f"0.3       = {c!r}")  # => co-03: shown for direct visual comparison against the sum above
    print(f"0.1 + 0.2 == 0.3: {total == c}")  # => co-03: expect False -- this is the headline claim
    assert total != c, "0.1 + 0.2 must NOT equal 0.3 in IEEE-754 binary64"  # => co-03: the structural fact
    assert repr(total) == "0.30000000000000004", "must print the exact documented value"  # => co-03: exact string
    print(f"Exact value printed: {total!r}")  # => co-03: confirms the precise digit string the syllabus names
    print(f"Decimal(0.1) reveals the TRUE stored binary value: {Decimal(a)}")  # => co-03: not exactly 0.1 at all
    # => co-03: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
