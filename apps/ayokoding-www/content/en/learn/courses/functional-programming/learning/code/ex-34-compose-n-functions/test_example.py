"""Example 34: pytest verification for compose(*fns) Folds a List of Functions."""

from example import add_one, compose, double, square


def test_compose_star_matches_nested_application_order() -> None:
    pipeline = compose(square, double, add_one)
    assert pipeline(3) == square(double(add_one(3))) == 64


# => Run: pytest -- Output: 1 passed
