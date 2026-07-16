# learning/code/ex-13-nand-completeness/nand_completeness.py
"""Example 13: NAND Completeness -- Building AND/OR/NOT from Only NAND."""  # => co-06: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-06: exhaustively checks every input combination against the builtin operators


def nand(a: bool, b: bool) -> bool:  # => co-06: the ONE primitive gate every other gate below is built from
    """The single primitive: NOT(a AND b)."""  # => co-06: documents nand's contract -- no runtime output, just sets its __doc__
    return not (a and b)  # => co-06: NAND's own definition -- the only gate this example is allowed to use directly


def not_from_nand(a: bool) -> bool:  # => co-06: NOT(a) = NAND(a, a) -- feeding the same input to both terminals
    return nand(a, a)  # => co-06: a AND a is just a, so NOT(a AND a) is NOT(a)


def and_from_nand(a: bool, b: bool) -> bool:  # => co-06: AND(a, b) = NOT(NAND(a, b)) -- double-negate a NAND
    return not_from_nand(nand(a, b))  # => co-06: built ENTIRELY from nand() and not_from_nand(), no `and`/`or`


def or_from_nand(a: bool, b: bool) -> bool:  # => co-06: OR(a, b) = NAND(NOT(a), NOT(b)) -- De Morgan via NAND
    return nand(not_from_nand(a), not_from_nand(b))  # => co-06: NAND of the two negations, per De Morgan's law


if __name__ == "__main__":  # => co-06: entry point -- this block runs only when the file executes directly, not on import
    for a, b in itertools.product([False, True], repeat=2):  # => co-06: all 4 combinations, exhaustive
        built_and, real_and = and_from_nand(a, b), a and b  # => co-06: NAND-built AND vs. Python's own `and`
        built_or, real_or = or_from_nand(a, b), a or b  # => co-06: NAND-built OR vs. Python's own `or`
        print(f"a={int(a)} b={int(b)}  AND={int(built_and)}  OR={int(built_or)}")  # => co-06: per-row report
        assert built_and == real_and, "NAND-built AND must match Python's builtin `and`"  # => co-06
        assert built_or == real_or, "NAND-built OR must match Python's builtin `or`"  # => co-06
    for a in (False, True):  # => co-06: NOT only takes one input -- checked separately, both cases
        assert not_from_nand(a) == (not a), "NAND-built NOT must match Python's builtin `not`"  # => co-06
    print("AND/OR/NOT built from NAND alone match the builtins on every input: True")  # => co-06: full proof
    # => co-06: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
