# learning/code/ex-01-first-passing-test/test_example.py
"""Example 1: First Passing Test."""


# ex-01: the smallest possible pytest test -- one function, one assert
# -- pytest discovers this file because it matches test_*.py (co-02)
# -- and discovers the function below because it matches test_* (co-02)
def add(a: int, b: int) -> int:  # => the unit under test: a plain, pure function
    return a + b  # => no test framework involvement at all inside the function itself


def test_adds() -> (
    None
):  # => the test function -- name MUST start with test_ to be discovered
    assert (
        add(2, 3) == 5
    )  # => arrange (2, 3) + act (call add) + assert, all on one line (co-01)
    # => if add(2, 3) had returned anything other than 5, pytest would report a failure here
