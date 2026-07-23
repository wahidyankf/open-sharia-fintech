# learning/code/ex-24-tdd-make-it-pass/test_example.py
"""Example 24: TDD Step 2 -- Green."""


# ex-24: TDD step 2 -- GREEN. The SAME test as ex-23, now with a MINIMAL implementation (co-17)
def clamp(value: int, minimum: int, maximum: int) -> int:  # => just enough code to pass  # fmt: skip
    if value < minimum:  # => branch 1: value is too low
        return minimum  # => clamp it UP to the floor
    if value > maximum:  # => branch 2: value is too high
        return maximum  # => clamp it DOWN to the ceiling
    return value  # => branch 3: value is already inside [minimum, maximum] -- leave it alone  # fmt: skip


def test_clamp_restricts_value_to_a_range() -> None:  # => IDENTICAL test body to ex-23's red version  # fmt: skip
    result = clamp(15, minimum=0, maximum=10)  # => now resolves -- clamp() exists in this file  # fmt: skip
    assert result == 10  # => 15 is above maximum=10, so it clamps DOWN to 10 -- now genuinely true  # fmt: skip
    # => this exact assertion was FALSE-BY-NONEXISTENCE in ex-23 (NameError) and is now
    # => a real, passing check -- red became green by adding the smallest correct implementation
