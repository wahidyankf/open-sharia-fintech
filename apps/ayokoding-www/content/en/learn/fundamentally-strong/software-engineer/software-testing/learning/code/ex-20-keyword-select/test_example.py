# learning/code/ex-20-keyword-select/test_example.py
"""Example 20: Keyword Selection with -k."""


# ex-20: four tests, only SOME of whose NAMES contain the substring "add" (co-08)
def add(a: int, b: int) -> int:  # => the unit under test for the matching tests
    return a + b  # => a plain pure function


def subtract(a: int, b: int) -> int:  # => a second, unrelated unit under test
    return a - b  # => used by the NON-matching tests below


def test_add_two_positives() -> None:  # => name CONTAINS "add" -- selected by -k "add"
    assert add(2, 3) == 5  # => passes


def test_add_negative_numbers() -> None:  # => name ALSO contains "add" -- also selected
    assert add(-2, -3) == -5  # => passes


def test_subtract_two_positives() -> None:  # => name does NOT contain "add" -- excluded
    assert subtract(5, 3) == 2  # => passes, but never runs under `pytest -k "add"`


def test_subtract_negative_numbers() -> None:  # => name does NOT contain "add" -- also excluded  # fmt: skip
    assert subtract(-5, -3) == -2  # => passes, but also skipped by the keyword filter
