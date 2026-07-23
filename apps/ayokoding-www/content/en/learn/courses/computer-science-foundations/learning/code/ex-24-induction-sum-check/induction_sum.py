# learning/code/ex-24-induction-sum-check/induction_sum.py
"""Example 24: Induction -- sum(1..n) == n(n+1)/2, Base Case + Inductive Step."""  # => co-14: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def closed_form(n: int) -> int:  # => co-14: the formula induction is used to PROVE, evaluated directly
    """Gauss's closed-form sum: 1 + 2 + ... + n = n(n+1)/2."""  # => co-14: documents closed_form's contract -- no runtime output, just sets its __doc__
    return n * (n + 1) // 2  # => co-14: integer division is exact here -- n(n+1) is always even


def base_case_holds() -> bool:  # => co-14: step 1 of induction -- the smallest instance, checked directly
    """Base case: n=1. sum(1..1) = 1, and closed_form(1) must also equal 1."""  # => co-14: documents base_case_holds's contract -- no runtime output, just sets its __doc__
    return sum(range(1, 2)) == closed_form(1)  # => co-14: sum(range(1,2)) is literally "1 + nothing else" = 1


def inductive_step_holds(k: int) -> bool:  # => co-14: step 2 -- ASSUMING it holds for k, prove it for k+1
    """Inductive step: IF closed_form(k) is correct, THEN closed_form(k+1) must also be correct."""  # => co-14: documents inductive_step_holds's contract -- no runtime output, just sets its __doc__
    assumed_sum_to_k = closed_form(k)  # => co-14: the inductive HYPOTHESIS -- assumed true, not re-derived
    sum_to_k_plus_1 = assumed_sum_to_k + (k + 1)  # => co-14: sum(1..k+1) = sum(1..k) + the ONE new term (k+1)
    return sum_to_k_plus_1 == closed_form(k + 1)  # => co-14: must equal the closed form evaluated at k+1


if __name__ == "__main__":  # => co-14: entry point -- this block runs only when the file executes directly, not on import
    print(f"base case (n=1) holds: {base_case_holds()}")  # => co-14: the induction's starting point
    assert base_case_holds(), "base case n=1 must hold"  # => co-14: induction cannot start without this
    failures: list[int] = []  # => co-14: records any k where the inductive step's implication fails
    for k in range(1, 1000):  # => co-14: "the reasoning template recursion mirrors" -- checked for k=1..999
        if not inductive_step_holds(k):  # => co-14: if the k->k+1 implication ever breaks, record it
            failures.append(k)  # => co-14: would mean the formula itself is wrong, not just untested
    print(f"inductive step checked for k=1..999, failures: {failures}")  # => co-14: expect an empty list
    assert failures == [], "the inductive step must hold for every k from 1 to 999"  # => co-14: no counterexample
    direct_sum_1000 = sum(range(1, 1001))  # => co-14: an INDEPENDENT brute-force check at the syllabus's n=1000
    print(f"sum(1..1000) direct = {direct_sum_1000}, closed_form(1000) = {closed_form(1000)}")  # => co-14
    assert direct_sum_1000 == closed_form(1000), "closed form must match brute-force sum at n=1000"  # => co-14
    print(f"Formula verified by induction for n up to 1000: True")  # => co-14: every check above passed
    # => co-14: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
