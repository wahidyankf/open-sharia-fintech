"""Example 17: Hand-Curry a Two-Argument Function."""

from typing import (
    Callable,
)  # => the return type of add_curried -- "a function int -> int"


def add(a: int, b: int) -> int:  # => the ordinary, uncurried, 2-argument function
    return a + b  # => both arguments supplied in a SINGLE call


def add_curried(
    a: int,
) -> Callable[[int], int]:  # => takes ONE argument, returns a function
    def inner(b: int) -> int:  # => the function waiting for the SECOND argument
        return a + b  # => a is captured from the enclosing scope, b arrives here

    return inner  # => add_curried(a) is itself a usable, partially-applied function


uncurried_result = add(2, 3)  # => the ordinary call -- both arguments at once
curried_result = add_curried(2)(3)  # => two separate calls: add_curried(2) THEN (3)

print(uncurried_result)  # => Output: 5
print(curried_result)  # => Output: 5
print(
    uncurried_result == curried_result
)  # => Output: True -- same computation, different shape

add_two = add_curried(
    2
)  # => a reusable, specialized function: "add 2 to whatever comes next"
print(add_two(10))  # => Output: 12
