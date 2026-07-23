"""Example 33: pytest verification for A Pipeline of partial Calls."""

from functools import partial

from example import offset, scale


def test_chained_partials_compose_like_ordinary_functions() -> None:
    double = partial(scale, 2)
    add_ten = partial(offset, 10)
    assert add_ten(double(5)) == 20
    assert double(100) == 200  # => double is reusable across any input


# => Run: pytest -- Output: 1 passed
