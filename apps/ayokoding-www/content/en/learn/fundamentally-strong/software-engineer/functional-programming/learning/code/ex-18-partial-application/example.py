"""Example 18: functools.partial Fixes an Argument."""

from functools import partial  # => stdlib's built-in way to pre-fill arguments


def power(base: int, exponent: int) -> int:  # => the general 2-argument function
    return base**exponent  # => base to the exponent power


square_of = partial(
    power, 2
)  # => fixes base=2, returns a 1-argument function of exponent
# => no lambda, no hand-written closure -- functools builds the wrapper for us

print(square_of(3))  # => Output: 8  (power(2, 3) == 2**3)
print(square_of(10))  # => Output: 1024  (power(2, 10) == 2**10)
print(
    power(2, 10) == square_of(10)
)  # => Output: True -- partial just pre-supplies base
