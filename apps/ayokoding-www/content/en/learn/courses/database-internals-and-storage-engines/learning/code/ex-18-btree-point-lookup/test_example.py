"""Example 18: pytest verification for B-Tree Point Lookup."""

from example import lookup


def test_present_key_is_found() -> None:
    assert lookup([10, 20, 30, 40, 50], 40) == 40


def test_absent_key_returns_none() -> None:
    assert lookup([10, 20, 30, 40, 50], 15) is None


# => Run: pytest -- Output: 2 passed
