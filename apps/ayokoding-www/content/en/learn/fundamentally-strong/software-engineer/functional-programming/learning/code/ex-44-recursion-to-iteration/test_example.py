"""Example 44: pytest verification for Converting Deep Recursion to an Explicit Stack."""

import sys

from example import sum_to_n_iterative, sum_to_n_recursive


def test_iterative_version_survives_a_depth_that_breaks_recursion() -> None:
    deep_n = sys.getrecursionlimit() + 500
    try:
        sum_to_n_recursive(deep_n)
        recursive_raised = False
    except RecursionError:
        recursive_raised = True
    assert recursive_raised is True

    assert sum_to_n_iterative(deep_n) == deep_n * (deep_n + 1) // 2


# => Run: pytest -- Output: 1 passed
