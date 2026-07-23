# learning/code/ex-26-test-pure-function/test_example.py
"""Example 26: Testing a Pure Function."""


# ex-26: a PURE function -- same input always gives the same output, no side effects (co-01, co-26)  # fmt: skip
def celsius_to_fahrenheit(celsius: float) -> float:  # => the unit under test
    return celsius * 9 / 5 + 32  # => a pure formula -- reads no state, writes no state


def test_freezing_point_of_water() -> None:  # => a well-known, easily-verified reference point  # fmt: skip
    assert (
        celsius_to_fahrenheit(0) == 32
    )  # => 0C is EXACTLY 32F -- an integer-clean case


def test_boiling_point_of_water() -> None:  # => a second well-known reference point
    assert (
        celsius_to_fahrenheit(100) == 212
    )  # => 100C is EXACTLY 212F -- also integer-clean


def test_a_negative_temperature() -> (
    None
):  # => confirms the formula works below zero too
    assert celsius_to_fahrenheit(-40) == -40  # => -40 is the ONE temperature where C and F agree  # fmt: skip


def test_calling_it_twice_gives_the_same_result() -> None:  # => directly demonstrates PURITY  # fmt: skip
    first_call = celsius_to_fahrenheit(37)  # => call 1, same input as call 2 below
    second_call = celsius_to_fahrenheit(37)  # => call 2, no state changed between calls
    assert (
        first_call == second_call
    )  # => a pure function can never disagree with itself (co-26)
