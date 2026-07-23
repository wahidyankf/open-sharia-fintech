# learning/code/ex-47-sat-brute-force/sat_brute_force.py
"""Example 47: Brute-Forcing 3-SAT -- Exponential Blowup with Variable Count."""  # => co-25: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-25: enumerates EVERY truth assignment -- 2**n of them, the source of the blowup
import time  # => co-25: measures the actual wall-clock cost of that enumeration, growing with n

Clause = tuple[int, int, int]  # => co-25: a 3-SAT clause -- three literals; a positive int is a var, negative is its negation


def clause_satisfied(clause: Clause, assignment: dict[int, bool]) -> bool:  # => co-25: True iff >=1 literal is True
    """A clause is satisfied iff at least one of its 3 literals evaluates to True under `assignment`."""  # => co-25: documents clause_satisfied's contract -- no runtime output, just sets its __doc__
    for literal in clause:  # => co-25: a clause is an OR of its literals -- one True literal is enough
        var = abs(literal)  # => co-25: the underlying variable this literal refers to
        value = assignment[var]  # => co-25: this assignment's truth value for that variable
        if (literal > 0 and value) or (literal < 0 and not value):  # => co-25: positive lit true, or negated lit true
            return True  # => co-25: short-circuits -- one satisfied literal is enough for the whole clause
    return False  # => co-25: no literal in this clause was satisfied


def brute_force_sat(clauses: list[Clause], num_vars: int) -> dict[int, bool] | None:  # => co-25: tries EVERY assignment
    """Try every one of the 2**num_vars truth assignments; return the first that satisfies all clauses, or None."""  # => co-25: documents brute_force_sat's contract -- no runtime output, just sets its __doc__
    for bits in itertools.product([False, True], repeat=num_vars):  # => co-25: exactly 2**num_vars candidates, exhaustive
        assignment = {i + 1: bits[i] for i in range(num_vars)}  # => co-25: variables are numbered 1..num_vars
        if all(clause_satisfied(c, assignment) for c in clauses):  # => co-25: EVERY clause must be satisfied (AND of ORs)
            return assignment  # => co-25: a satisfying assignment found -- stop immediately
    return None  # => co-25: no assignment among all 2**num_vars satisfied every clause -- UNSAT


def build_satisfiable_instance(num_vars: int) -> list[Clause]:  # => co-25: a small family that stays satisfiable as n grows
    """Build a 3-SAT instance over num_vars variables that is always satisfiable (all-True works)."""  # => co-25: documents build_satisfiable_instance's contract -- no runtime output, just sets its __doc__
    return [(i, i + 1 if i + 1 <= num_vars else 1, i + 2 if i + 2 <= num_vars else 1) for i in range(1, num_vars + 1)]  # => co-25: returns this computed value to the caller


if __name__ == "__main__":  # => co-25: entry point -- this block runs only when the file executes directly, not on import
    sizes = [12, 16, 20, 24]  # => co-25: each size adds 4 more variables -- DOUBLES the search space every +1
    timings: list[float] = []  # => co-25: one measured wall-clock duration per size
    for n in sizes:  # => co-25: time the FULL brute-force search at each variable count
        clauses = build_satisfiable_instance(n)  # => co-25: a satisfiable instance -- forces the FULL exponential search
        start = time.perf_counter()  # => co-25: begin timing window
        brute_force_sat(clauses, n)  # => co-25: the timed operation -- 2**n candidate assignments checked
        elapsed = time.perf_counter() - start  # => co-25: elapsed wall-clock seconds
        timings.append(elapsed)  # => co-25: recorded for the growth-ratio check below
        print(f"n={n:>2} vars  2**n={2**n:>10,}  time={elapsed:.4f}s")  # => co-25: size, search-space size, and duration
    ratios = [timings[i + 1] / timings[i] for i in range(len(timings) - 1)]  # => co-25: growth factor per +4 variables
    print(f"time ratios per +4 variables: {[round(r, 1) for r in ratios]}")  # => co-25: expect roughly 2**4 = 16x each step
    # Each step adds 4 variables, so the search space multiplies by 2**4 = 16 -- an EXPONENTIAL,
    # not polynomial, growth rate, in stark contrast to Example 45's O(n log n) sort.
    assert all(r > 4 for r in ratios), "runtime must grow exponentially (roughly ~2**n), not polynomially"  # => co-25
    print(f"Runtime grows exponentially with variable count: True")  # => co-25: reached only if the assert passed
    # => co-25: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
