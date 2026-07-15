# learning/code/ex-04-run-single-test/test_example.py
"""Example 4: Run a Single Test by Name."""


# ex-04: THREE tests in one file -- run only ONE of them by name (co-02)
def square(n: int) -> int:  # => the unit under test
    return n * n  # => a pure function, reused by all three tests below


def test_square_of_two() -> None:  # => test A -- the one we will select by name below
    assert square(2) == 4  # => 2*2 -- passes


def test_square_of_three() -> None:  # => test B -- deliberately NOT selected below
    assert square(3) == 9  # => 3*3 -- passes, but never runs in this example's command


def test_square_of_negative() -> None:  # => test C -- also NOT selected below
    assert square(-4) == 16  # => (-4)*(-4) -- passes, but also skipped by the selector
