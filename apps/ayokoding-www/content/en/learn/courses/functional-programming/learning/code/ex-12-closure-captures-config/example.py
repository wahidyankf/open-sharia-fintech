"""Example 12: A Closure Capturing a Threshold."""

from typing import (
    Callable,
)  # => the return type of make_validator -- "a function int -> bool"


def make_validator(
    threshold: int,
) -> Callable[[int], bool]:  # => bakes threshold into a closure
    def is_above_threshold(
        value: int,
    ) -> bool:  # => captures threshold, no parameter for it
        return (
            value > threshold
        )  # => reads the ENCLOSING threshold, not a fresh argument

    return (
        is_above_threshold  # => this closure, not a plain value, is what gets returned
    )


passes_ten = make_validator(10)  # => remembers threshold=10 forever
passes_hundred = make_validator(100)  # => a DIFFERENT closure, remembers threshold=100

print(passes_ten(15))  # => Output: True   (15 > 10)
print(passes_hundred(15))  # => Output: False  (15 is NOT > 100)
print(
    passes_ten(15) != passes_hundred(15)
)  # => Output: True -- same input, different config
