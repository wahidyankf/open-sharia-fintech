"""Example 21: the workload this example's pre-generated flame graph was sampled from."""

from __future__ import annotations


def deep_recursion(n: int) -> int:
    """One call in a DEEP (40-frame) recursive chain."""
    if n <= 0:
        return 0
    return 1 + deep_recursion(n - 1)


def deep_phase() -> int:
    """TALL but not the widest: many deep, cheap calls -- a deep stack, modest total time."""
    total = 0
    for _ in range(150_000):
        total += deep_recursion(40)
    return total


def hot_loop() -> int:
    """WIDE and hot: a shallow loop that owns most of this program's total sampled time."""
    total = 0
    for i in range(60_000_000):
        total += i
    return total


def run_workload() -> None:
    deep_phase()
    hot_loop()
