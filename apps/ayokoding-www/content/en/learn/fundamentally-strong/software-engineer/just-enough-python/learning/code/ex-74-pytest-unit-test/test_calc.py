"""Example 74: pytest unit test for calc.add."""

from calc import add  # => imports the function under test


# pytest discovers any function named test_* automatically.
def test_add() -> None:
    # A bare assert -- pytest reports failures with a full diff.
    assert add(2, 3) == 5  # => passes because add(2, 3) really does equal 5


# => Run: pytest -- Output: 1 passed
