# learning/code/ex-14-parametrize-cases/test_example.py
"""Example 14: Parametrize Three Cases."""

import pytest  # => brings in @pytest.mark.parametrize (co-06)


def double(n: int) -> int:  # => the unit under test
    return (
        n * 2
    )  # => a pure function -- exactly what parametrize is best suited to exercise


@pytest.mark.parametrize(  # => starts the parametrize call -- ids are inferred below (Example 15 gives them explicitly)  # fmt: skip
    "input_value, expected",  # => two parameter NAMES, matched to the test function's args
    [  # => the list of rows -- each tuple below becomes one independently-reported test case  # fmt: skip
        (1, 2),  # => row 1: double(1) should be 2
        (2, 4),  # => row 2: double(2) should be 4
        (10, 20),  # => row 3: double(10) should be 20
    ],
)  # => end of parametrize's argument list -- three rows queued above  # fmt: skip
def test_double_over_three_rows(input_value: int, expected: int) -> None:  # => the SAME body runs once per row  # fmt: skip
    # => pytest runs THIS ONE function body three separate times, once per row above,
    # => reporting each row as its OWN pass/fail case in the output (co-06)
    assert double(input_value) == expected  # => act+assert, identical logic, different data each run  # fmt: skip
