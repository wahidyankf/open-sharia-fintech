"""Example 20: A Left-to-Right pipe Helper."""

from functools import reduce  # => reduce folds *fns into x one step at a time
from typing import Callable  # => the type of each step function pipe accepts


def pipe(
    x: int, *fns: Callable[[int], int]
) -> int:  # => *fns: any number of step functions
    return reduce(
        lambda acc, fn: fn(acc), fns, x
    )  # => applies each fn IN ORDER, left to right


def add_one(x: int) -> int:  # => the first step in the pipeline below
    return x + 1  # => adds exactly one


def double(x: int) -> int:  # => the second step in the pipeline below
    return x * 2  # => doubles its argument


piped_result = pipe(
    3, add_one, double
)  # => reads top-to-bottom: start at 3, add_one, THEN double
nested_result = double(
    add_one(3)
)  # => the equivalent nested call -- reads inside-out instead

print(piped_result)  # => Output: 8
print(nested_result)  # => Output: 8
print(
    piped_result == nested_result
)  # => Output: True -- pipe and nesting compute the same thing
