# learning/code/ex-02-failing-test-output/test_example.py
"""Example 2: Failing Test Output."""


# ex-02: a DELIBERATELY wrong assertion -- this test is meant to fail
# -- the point is to see pytest's expression introspection, not to pass (co-03)
def add(a: int, b: int) -> int:  # => the same pure function as ex-01
    return (
        a + b
    )  # => genuinely returns 5 for add(2, 3) -- the test below expects 6 instead


def test_adds_wrong_expectation() -> None:  # => named honestly -- this SHOULD fail
    assert (
        add(2, 3) == 6
    )  # => plain assert -- pytest rewrites this at import time (co-03)
    # => pytest's assertion rewriting inspects BOTH sides of == and shows the actual
    # => value (5) next to the expected literal (6), with no assertNotEqual-style API needed
