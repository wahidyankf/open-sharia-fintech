"""Example 34: compose(*fns) Folds a List of Functions."""

from functools import reduce  # => reduce folds the chain of functions inside compose
from typing import Callable  # => Callable types every function compose accepts


def compose(
    *fns: Callable[[int], int],
) -> Callable[[int], int]:  # => any NUMBER of functions
    def composed(x: int) -> int:  # => the returned pipeline function
        return reduce(
            lambda acc, fn: fn(acc), reversed(fns), x
        )  # => rightmost fn runs FIRST
        # => reversed(fns) makes compose(f, g, h)(x) mean f(g(h(x))), matching math notation

    return composed  # => compose itself returns the pipeline function, not a value


def add_one(x: int) -> int:  # => the innermost step in the pipeline below
    return x + 1  # => the actual +1 add_one performs


def double(x: int) -> int:  # => the middle step in the pipeline below
    return x * 2  # => the actual *2 double performs


def square(x: int) -> int:  # => the outermost step in the pipeline below
    return x * x  # => the actual squaring square performs


pipeline = compose(
    square, double, add_one
)  # => reads right-to-left: square(double(add_one(x)))
result = pipeline(3)  # => add_one(3)=4, double(4)=8, square(8)=64

print(result)  # => Output: 64
print(
    result == square(double(add_one(3)))
)  # => Output: True -- compose(*fns) matches nested calls
