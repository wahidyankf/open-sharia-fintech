"""Kata 4 (after): composition-order fix -- pipe() runs left-to-right, matching the reading order."""

from functools import reduce
from typing import Callable


def pipe(x: int, *fns: Callable[[int], int]) -> int:
    return reduce(
        lambda acc, fn: fn(acc), fns, x
    )  # => applies fns in ORDER, left to right


def add_one(x: int) -> int:
    return x + 1


def double(x: int) -> int:
    return x * 2


# INTENT: "add one, THEN double" -- pipe(5, add_one, double) reads AND runs left to right.
result = pipe(5, add_one, double)  # => add_one(5)=6 runs first, then double(6)=12
print(result)
