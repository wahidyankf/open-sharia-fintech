"""Kata 4 (before): composition-order bug -- compose() runs right-to-left, not the intended order."""

from typing import Callable


def compose(f: Callable[[int], int], g: Callable[[int], int]) -> Callable[[int], int]:
    return lambda x: f(
        g(x)
    )  # => g runs FIRST, then f -- right-to-left, mathematical convention


def add_one(x: int) -> int:
    return x + 1


def double(x: int) -> int:
    return x * 2


# INTENT: "add one, THEN double" -- reading compose(add_one, double) left to right like a pipe call.
transform = compose(
    add_one, double
)  # SMELL: reads left-to-right but compose runs right-to-left
result = transform(
    5
)  # BUG: double(5) runs FIRST giving 10, then add_one gives 11 -- not (5+1)*2=12
print(result)
