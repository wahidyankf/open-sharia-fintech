# learning/code/ex-17-mark-skip/test_example.py
"""Example 17: Mark a Test skip."""

import pytest  # => brings in @pytest.mark.skip, a BUILTIN marker needing no registration (co-08)


def divide(a: int, b: int) -> float:  # => the unit under test
    return a / b  # => raises ZeroDivisionError if b == 0 -- not handled here on purpose


def test_divide_normal_case() -> None:  # => runs normally -- included only for contrast
    assert divide(10, 2) == 5.0  # => a plain, unskipped assertion


@pytest.mark.skip(reason="division-by-zero handling not implemented yet")  # => co-08: skip, with a REQUIRED-by-convention reason string  # fmt: skip
def test_divide_by_zero_not_yet_supported() -> None:
    # => pytest never even EXECUTES this function body -- it is reported as "skipped"
    # => before a single line inside it runs, which is why this can safely contain
    # => code that would otherwise crash (ZeroDivisionError) without failing the suite
    assert divide(10, 0) == float("inf")  # => this line never actually runs -- entirely skipped  # fmt: skip
