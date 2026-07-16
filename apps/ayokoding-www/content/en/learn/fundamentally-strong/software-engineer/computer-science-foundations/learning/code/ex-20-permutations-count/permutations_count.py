# learning/code/ex-20-permutations-count/permutations_count.py
"""Example 20: nPr -- Counting Permutations and Enumerating Them."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-12: itertools.permutations does the actual enumeration this example counts
import math  # => co-12: math.factorial computes n! and (n-r)! for the closed-form count


def npr(n: int, r: int) -> int:  # => co-12: the closed-form permutation-count formula
    """Count r-permutations of n items: n! / (n - r)!."""  # => co-12: documents npr's contract -- no runtime output, just sets its __doc__
    return math.factorial(n) // math.factorial(n - r)  # => co-12: order MATTERS -- this is why it's n!/(n-r)!, not nCr


if __name__ == "__main__":  # => co-12: entry point -- this block runs only when the file executes directly, not on import
    n, r = 6, 3  # => co-12: 6 items, choose and ORDER 3 of them
    formula_count = npr(n, r)  # => co-12: the closed-form answer
    enumerated = list(itertools.permutations(range(n), r))  # => co-12: every actual r-length ordered tuple
    enumerated_count = len(enumerated)  # => co-12: counted by ENUMERATION, independent of the formula
    print(f"n={n} r={r}")  # => co-12: states the parameters being counted
    print(f"nPr formula = {n}! / ({n}-{r})! = {formula_count}")  # => co-12: prints the formula's result
    print(f"enumerated permutations count = {enumerated_count}")  # => co-12: prints the enumeration's result
    print(f"first 3 permutations: {enumerated[:3]}")  # => co-12: a small sample, to show what's being counted
    assert enumerated_count == formula_count, "enumeration count must match n!/(n-r)!"  # => co-12: the actual proof
    assert formula_count == 120, "6P3 must equal 120"  # => co-12: a fixed, independently-checkable number
    print(f"Count matches n!/(n-r)!: True")  # => co-12: reached only if both asserts passed
    # => co-12: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
