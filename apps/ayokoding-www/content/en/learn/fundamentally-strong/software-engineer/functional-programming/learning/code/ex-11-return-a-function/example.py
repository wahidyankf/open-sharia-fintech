"""Example 11: A Function Returning a Closure."""

from typing import (
    Callable,
)  # => the return type of multiplier -- "a function int -> int"


def multiplier(
    n: int,
) -> Callable[[int], int]:  # => HOF: RETURNS a function, doesn't just take one
    def multiply_by_n(
        x: int,
    ) -> int:  # => a closure -- captures n from the enclosing scope
        return x * n  # => n is remembered even after multiplier() has already returned

    return multiply_by_n  # => the inner function itself is the return value


times_three = multiplier(
    3
)  # => times_three is now a function that always multiplies by 3
times_five = multiplier(5)  # => a SEPARATE closure, capturing a different n (5)

print(times_three(4))  # => Output: 12  (4 * 3, using the captured n=3)
print(times_five(4))  # => Output: 20  (4 * 5, using the captured n=5)
print(
    multiplier(3)(4) == 12
)  # => Output: True -- calling the returned function immediately
