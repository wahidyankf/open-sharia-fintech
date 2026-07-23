# learning/code/ex-03-arrange-act-assert/test_example.py
"""Example 3: Arrange-Act-Assert."""


# ex-03: the SAME test as ex-01, restructured into three visually distinct phases (co-01)
# -- AAA is a convention, not a pytest feature -- nothing here is pytest-specific syntax
def multiply(a: int, b: int) -> int:  # => the unit under test
    return a * b  # => a pure function -- no I/O, no hidden state (co-26)


def test_multiply_arrange_act_assert() -> None:
    # --- Arrange: build the inputs the test needs, named clearly ---
    first_factor = 6  # => arrange phase, part 1: a plain input value
    second_factor = 7  # => arrange phase, part 2: a second plain input value
    expected = 42  # => arrange phase, part 3: the expected RESULT, computed by hand

    # --- Act: call the ONE thing under test, exactly once ---
    actual = multiply(first_factor, second_factor)  # => act phase -- the single call being tested  # fmt: skip

    # --- Assert: compare what happened against what was expected ---
    assert (
        actual == expected
    )  # => assert phase -- the only line that can fail this test
