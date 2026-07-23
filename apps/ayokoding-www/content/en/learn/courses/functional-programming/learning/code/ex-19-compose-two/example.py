"""Example 19: A compose(f, g) Helper."""

from typing import Callable  # => the type of every function this example composes


def compose(  # => a HOF: takes two functions, RETURNS a new function
    f: Callable[[int], int],
    g: Callable[[int], int],  # => the two functions being combined
) -> Callable[[int], int]:  # => the return type -- itself a function int -> int
    def composed(x: int) -> int:  # => the returned function -- runs g FIRST, then f
        return f(g(x))  # => g(x) computed first; its result feeds into f

    return composed  # => composed itself, not a value, is compose's return value


def add_one(x: int) -> int:  # => one of the two small functions being composed together
    return x + 1  # => adds exactly one


def double(x: int) -> int:  # => the other small function being composed together
    return x * 2  # => doubles its argument


add_then_double = compose(double, add_one)  # => reads right-to-left: double(add_one(x))
result = add_then_double(3)  # => add_one(3) is 4, then double(4) is 8

print(result)  # => Output: 8
print(
    add_then_double(3) == double(add_one(3))
)  # => Output: True -- compose just names f(g(x))
