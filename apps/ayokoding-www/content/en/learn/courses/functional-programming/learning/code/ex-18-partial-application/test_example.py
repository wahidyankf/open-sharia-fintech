"""Example 18: pytest verification for functools.partial Fixes an Argument."""

from functools import partial

from example import power


def test_partial_fixes_the_first_argument() -> None:
    square_of = partial(power, 2)
    assert square_of(10) == power(2, 10) == 1024


# => Run: pytest -- Output: 1 passed
