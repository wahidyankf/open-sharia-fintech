"""Example 10: A Higher-Order apply Function."""

from typing import Callable  # => the type of "a function taking int, returning int"


def apply(
    fn: Callable[[int], int], x: int
) -> int:  # => HOF: takes a FUNCTION as an argument
    return fn(x)  # => apply never needs to know what fn actually does


def increment(n: int) -> int:  # => one candidate to pass into apply
    return n + 1  # => adds exactly one


def triple(n: int) -> int:  # => a second, unrelated candidate to pass into apply
    return n * 3  # => multiplies by three


result_increment = apply(increment, 10)  # => apply calls increment(10) internally
result_triple = apply(triple, 10)  # => same apply, DIFFERENT function passed in

print(result_increment)  # => Output: 11
print(result_triple)  # => Output: 30
print(
    apply(increment, 10) == increment(10)
)  # => Output: True -- apply just forwards the call
