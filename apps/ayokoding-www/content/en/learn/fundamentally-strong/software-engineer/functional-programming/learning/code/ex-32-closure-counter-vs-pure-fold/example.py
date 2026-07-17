"""Example 32: Stateful Closure Counter vs. Pure Fold."""

from functools import reduce  # => reduce is used by the pure fold below
from typing import Callable  # => Callable types the closure returned by make_counter


def make_counter() -> Callable[[], int]:  # => returns a closure holding MUTABLE state
    count = 0  # => lives INSIDE the closure -- state lives here, nowhere else

    def increment() -> int:  # => the returned closure itself
        nonlocal count  # => declares intent to mutate the ENCLOSING count, not a local copy
        count += 1  # => side effect: mutates state captured by the closure
        return count  # => returns the count AFTER incrementing

    return increment  # => make_counter itself returns the closure, not a value


def count_pure(
    n: int,
) -> int:  # => a pure fold: no closure, no mutation, no hidden state
    return reduce(
        lambda acc, _: acc + 1, range(n), 0
    )  # => the SAME total, computed with zero state


counter = make_counter()  # => a fresh closure with its own private count
stateful_result = [
    counter(),
    counter(),
    counter(),
]  # => each call MUTATES the shared closure state
pure_result = count_pure(
    3
)  # => a single expression, no calls needed, no state anywhere

# => co-08 closures vs co-01 purity: same answer, two different state models
print(stateful_result)  # => Output: [1, 2, 3]
print(pure_result)  # => Output: 3
print(
    stateful_result[-1] == pure_result
)  # => Output: True -- same final count, different state model
