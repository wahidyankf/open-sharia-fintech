"""Example 33: A Pipeline of partial Calls."""

from functools import partial  # => partial is the currying mechanism used below


def scale(
    factor: int, x: int
) -> int:  # => a 2-argument function -- factor fixed, x supplied later
    return factor * x  # => the actual multiplication scale performs


def offset(amount: int, x: int) -> int:  # => a second 2-argument function, same shape
    return amount + x  # => the actual addition offset performs


double = partial(scale, 2)  # => fixes factor=2 -- a reusable "double" function
add_ten = partial(offset, 10)  # => fixes amount=10 -- a reusable "add ten" function

pipeline_result = add_ten(double(5))  # => double(5) is 10, then add_ten(10) is 20
manual_result = 10 + (
    2 * 5
)  # => the equivalent hand-written arithmetic, for comparison

# => partial is Python's practical stand-in for true currying (co-10)
print(pipeline_result)  # => Output: 20
print(
    pipeline_result == manual_result
)  # => Output: True -- partials compose like ordinary functions
print(double(100))  # => Output: 200 -- double is REUSABLE across any input, not just 5
