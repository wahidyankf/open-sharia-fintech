# learning/code/ex-52-coverage-line-report/test_example.py
"""Example 52: A Line Coverage Report."""


# ex-52: coverage.py 7.15.1 measures which LINES actually ran during a test session (co-21, co-27)  # fmt: skip
def add(a: int, b: int) -> int:  # => the unit under test -- WILL be exercised by the test below  # fmt: skip
    return a + b  # => this line runs, and coverage.py records it as covered


def subtract(a: int, b: int) -> int:  # => a SECOND function -- deliberately left UNTESTED here  # fmt: skip
    return (
        a - b
    )  # => this line NEVER runs in this file -- coverage.py reports it as MISSING


def test_add_is_covered() -> None:  # => the ONLY test in this file -- exercises add(), not subtract()  # fmt: skip
    assert add(2, 3) == 5  # => causes line 5 (add's return) to run -- subtract's line 9 never does  # fmt: skip
