"""Example 2: pytest verification for Theta vs O Classification."""

from example import constant_cost, doubling_ratio, linear_cost, quadratic_cost


def test_constant_cost_ratio_is_one() -> None:
    assert doubling_ratio(constant_cost) == 1.0  # => O(1) never grows with n


def test_linear_cost_ratio_is_two() -> None:
    assert doubling_ratio(linear_cost) == 2.0  # => O(n) doubles when n doubles


def test_quadratic_cost_ratio_is_four() -> None:
    assert doubling_ratio(quadratic_cost) == 4.0  # => O(n^2) quadruples


# => Run: pytest -- Output: 3 passed
