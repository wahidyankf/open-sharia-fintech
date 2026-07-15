# learning/code/ex-08-raises-valueerror/test_example.py
"""Example 8: Raises ValueError."""

import pytest  # => brings in pytest.raises, the exception-testing context manager (co-04)


def parse_positive_int(text: str) -> int:  # => the unit under test
    value = int(
        text
    )  # => may itself raise ValueError for non-numeric text -- not caught here
    if value <= 0:  # => a SECOND way to reach the same exception type
        raise ValueError(
            f"expected a positive integer, got {value}"
        )  # => explicit raise
    return value  # => only reached when value is a genuine positive integer


def test_raises_valueerror_on_non_positive_input() -> None:
    with pytest.raises(ValueError):  # => wraps the call -- the block must raise EXACTLY this  # fmt: skip
        parse_positive_int(
            "-5"
        )  # => act: -5 is not positive, so ValueError fires as expected
    # => if parse_positive_int("-5") had returned normally instead of raising, this test
    # => would fail with "DID NOT RAISE ValueError" -- pytest.raises checks BOTH directions
