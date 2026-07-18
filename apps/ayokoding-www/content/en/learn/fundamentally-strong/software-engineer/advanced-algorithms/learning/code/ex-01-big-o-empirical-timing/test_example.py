"""Example 1: pytest verification for Big-O Empirical Timing."""

from example import linear_scan, quadratic_scan


def test_linear_scan_counts_exactly_n_steps() -> None:
    assert linear_scan(50) == 50  # => an O(n) pass takes exactly n steps


def test_quadratic_scan_counts_n_squared_steps() -> None:
    assert quadratic_scan(50) == 2500  # => an O(n^2) pass takes n*n steps


def test_quadratic_grows_faster_than_linear_as_n_doubles() -> None:
    small_ratio = quadratic_scan(20) / linear_scan(20)  # => 20x at n=20
    large_ratio = quadratic_scan(40) / linear_scan(40)  # => 40x at n=40 (n doubled)
    assert large_ratio > small_ratio  # => the quadratic-to-linear gap widens with n


# => Run: pytest -- Output: 3 passed
