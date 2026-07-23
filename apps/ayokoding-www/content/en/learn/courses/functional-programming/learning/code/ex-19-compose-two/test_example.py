"""Example 19: pytest verification for A compose(f, g) Helper."""

from example import add_one, compose, double


def test_compose_runs_g_then_f() -> None:
    add_then_double = compose(double, add_one)
    assert add_then_double(3) == double(add_one(3)) == 8


# => Run: pytest -- Output: 1 passed
