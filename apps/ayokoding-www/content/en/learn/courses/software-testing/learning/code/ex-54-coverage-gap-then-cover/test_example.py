# learning/code/ex-54-coverage-gap-then-cover/test_example.py
"""Example 54: Closing a Coverage Gap."""


# ex-54: ONE file, run twice -- first with a coverage GAP, then with it CLOSED (co-21)
def calculate_shipping(weight: float) -> float:  # => the unit under test -- has TWO paths  # fmt: skip
    if weight <= 5:  # => branch 1: light packages
        return 5.00  # => flat rate -- exercised by test_light_package below
    else:  # => branch 2: heavy packages -- INITIALLY uncovered in this narrative
        return 5.00 + (weight - 5) * 0.50  # => surcharge per extra kg -- the GAP this example closes  # fmt: skip


def test_light_package() -> None:  # => run ALONE first (via -k), this leaves the else branch uncovered  # fmt: skip
    assert calculate_shipping(3) == 5.00  # => only ever exercises the if-branch above


def test_heavy_package() -> None:  # => added SECOND -- running the WHOLE file closes the gap  # fmt: skip
    assert calculate_shipping(10) == 7.50  # => 5.00 + (10-5)*0.50 -- exercises the else-branch's line  # fmt: skip
