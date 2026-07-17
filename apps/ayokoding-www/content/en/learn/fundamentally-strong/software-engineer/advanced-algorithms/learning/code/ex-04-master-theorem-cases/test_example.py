"""Example 4: pytest verification for the Master Theorem's Three Cases."""

from example import classify_master_case, critical_exponent


def test_case1_when_f_grows_slower_than_split() -> None:
    assert classify_master_case(a=8, b=2, f_exponent=1) == "case1"  # => 8T(n/2)+n


def test_case2_when_f_matches_split_exactly() -> None:
    assert classify_master_case(a=2, b=2, f_exponent=1) == "case2"  # => merge sort


def test_case3_when_f_grows_faster_than_split() -> None:
    assert classify_master_case(a=2, b=2, f_exponent=2) == "case3"  # => 2T(n/2)+n^2


def test_critical_exponent_matches_known_values() -> None:
    assert critical_exponent(8, 2) == 3.0  # => log_2(8) = 3
    assert critical_exponent(2, 2) == 1.0  # => log_2(2) = 1


# => Run: pytest -- Output: 4 passed
