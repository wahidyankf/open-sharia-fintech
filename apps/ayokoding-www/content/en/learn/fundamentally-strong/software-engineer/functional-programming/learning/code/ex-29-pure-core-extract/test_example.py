"""Example 29: pytest verification for Extract a Pure Core from a Mutating Routine."""

from example import make_log_lines, sum_orders_pure


def test_pure_core_needs_no_mocking() -> None:
    orders = [1, 2, 3]
    assert (
        sum_orders_pure(orders) == 6
    )  # => tested with plain arguments, no I/O to intercept


def test_log_lines_extracted_as_pure_function() -> None:
    orders = [5, 15]
    assert make_log_lines(orders) == ["processed 5", "processed 15"]


# => Run: pytest -- Output: 2 passed
