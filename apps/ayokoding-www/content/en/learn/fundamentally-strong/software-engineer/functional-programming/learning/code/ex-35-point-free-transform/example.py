"""Example 35: Rewriting a Lambda Pipeline Point-Free."""

from functools import (
    partial,
    reduce,
)  # => partial curries add/multiply; reduce powers compose
from typing import (
    Callable,
)  # => Callable types the pipeline function returned by compose


def compose(
    *fns: Callable[[int], int],
) -> Callable[[int], int]:  # => folds fns right-to-left
    def composed(x: int) -> int:  # => the returned pipeline function
        return reduce(
            lambda acc, fn: fn(acc), reversed(fns), x
        )  # => rightmost fn runs FIRST, matching math notation

    return composed  # => compose itself returns the pipeline function


def add(n: int, x: int) -> int:  # => a 2-argument helper, curried via partial below
    return n + x  # => the actual addition add performs


def multiply(n: int, x: int) -> int:  # => a second 2-argument helper, same shape
    return n * x  # => the actual multiplication multiply performs


with_named_arg: Callable[[int], int] = lambda x: multiply(
    2, add(3, x)
)  # => POINTED: names x explicitly
point_free = compose(
    partial(multiply, 2), partial(add, 3)
)  # => POINT-FREE: x never named

# => point-free style trades explicit naming for compact composition (co-19)
print(with_named_arg(5))  # => Output: 16  ((5 + 3) * 2)
print(
    point_free(5)
)  # => Output: 16 -- identical result, x never appears in point_free's own definition
print(
    with_named_arg(5) == point_free(5)
)  # => Output: True -- two styles, one computation
