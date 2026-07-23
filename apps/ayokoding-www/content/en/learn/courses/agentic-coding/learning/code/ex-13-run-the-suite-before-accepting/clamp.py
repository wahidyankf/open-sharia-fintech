# learning/code/ex-13-run-the-suite-before-accepting/clamp.py
"""Example ex-13: candidate implementations of clamp() -- v1 (buggy) and v2 (fixed)."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def clamp_v1(value: float, low: float, high: float) -> float:  # => co-13: the agent's FIRST diff -- only implements half the requirement
    """Clamp `value` into [low, high] (buggy: never raises a below-range value up to low)."""  # => co-13: documents the (wrong) contract this diff actually implements
    return min(value, high)  # => co-13: BUG -- clamps the upper bound only; a value below `low` passes straight through unchanged


def clamp_v2(value: float, low: float, high: float) -> float:  # => co-13: the agent's SECOND diff -- the fix, after the suite rejected v1
    """Clamp `value` into [low, high] (fixed: both bounds are enforced)."""  # => co-13: documents the contract this diff actually implements
    return max(low, min(value, high))  # => co-13: clamps the upper bound first, then raises the result up to `low` if still too small
