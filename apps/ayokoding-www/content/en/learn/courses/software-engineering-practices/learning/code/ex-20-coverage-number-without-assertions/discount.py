# learning/code/ex-20-coverage-number-without-assertions/discount.py
"""ex-20: a function with a real bug, still reachable at 100% line coverage (co-12)."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def apply_discount(total: float, pct: float) -> float:  # => co-12: the function under test
    return total * pct  # => co-12: BUG -- should be total * (1 - pct); a 20% discount on $100
    # => co-12: should return $80, this returns $20 -- the discount and the KEPT amount are swapped
