# learning/code/ex-49-tsp-factorial-demo/tsp_factorial.py
"""Example 49: Brute-Force TSP -- Factorial Growth in the Number of Tours."""  # => co-24: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-24, co-25: itertools.permutations enumerates every possible visiting order, exhaustively
import math  # => co-24: math.factorial computes the closed-form (n-1)! tour count to check the enumeration against


def all_tours(cities: list[str]) -> list[tuple[str, ...]]:  # => co-24: brute-force TSP -- every possible tour, fixed start
    """Enumerate every distinct tour starting from cities[0] (a fixed start eliminates rotations)."""  # => co-24: documents all_tours's contract -- no runtime output, just sets its __doc__
    start, rest = cities[0], cities[1:]  # => co-24: fixing the start city is the standard (n-1)! reduction
    return [(start, *perm) for perm in itertools.permutations(rest)]  # => co-25: (n-1)! orderings of the remaining cities


if __name__ == "__main__":  # => co-25: entry point -- this block runs only when the file executes directly, not on import
    for n in (4, 5, 6, 7):  # => co-24: a small spread of city counts, small enough to enumerate directly
        cities = [f"city{i}" for i in range(n)]  # => co-24: n distinct city labels
        tours = all_tours(cities)  # => co-25: EVERY possible tour, brute-force enumerated
        expected_count = math.factorial(n - 1)  # => co-24: the closed-form tour count -- (n-1)!, fixed start
        print(f"n={n} cities -> {len(tours)} tours enumerated, (n-1)! = {expected_count}")  # => co-24: side by side
        assert len(tours) == expected_count, f"tour count for n={n} must equal (n-1)! = {expected_count}"  # => co-24
    growth_4_to_7 = math.factorial(6) / math.factorial(3)  # => co-25: (7-1)! / (4-1)! -- how much the count exploded
    print(f"tour count growth from n=4 to n=7: {growth_4_to_7:.0f}x")  # => co-25: factorial, not polynomial, growth
    assert growth_4_to_7 > 100, "the tour count must grow FACTORIALLY, not polynomially, as n increases"  # => co-25
    print(f"Tour count exactly matches (n-1)! at every tested size: True")  # => co-24, co-25: every assert passed
    # => co-25: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
