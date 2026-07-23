"""Example 47: pytest verification for case Clauses With if Guards."""

from example import classify


def test_guards_select_the_right_branch() -> None:
    assert classify(-1) == "negative"
    assert classify(0) == "zero"
    assert classify(2) == "positive even"
    assert classify(3) == "positive odd"


# => Run: pytest -- Output: 1 passed
