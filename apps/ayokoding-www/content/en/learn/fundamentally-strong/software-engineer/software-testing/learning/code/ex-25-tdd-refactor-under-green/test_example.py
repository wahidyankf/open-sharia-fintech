# learning/code/ex-25-tdd-refactor-under-green/test_example.py
"""Example 25: TDD Step 3 -- Refactor."""


# ex-25: TDD step 3 -- REFACTOR. Same test, DIFFERENT (shorter) implementation (co-17)
def clamp(value: int, minimum: int, maximum: int) -> int:  # => refactored: one expression  # fmt: skip
    # => max(minimum, ...) rules out anything below the floor; min(maximum, ...) then rules
    # => out anything above the ceiling -- functionally IDENTICAL to ex-24's three branches
    return max(minimum, min(maximum, value))  # => a single line replaces three if/return statements  # fmt: skip


def test_clamp_restricts_value_to_a_range() -> None:  # => the EXACT SAME test as ex-23 and ex-24  # fmt: skip
    result = clamp(15, minimum=0, maximum=10)  # => still resolves to 10 -- behavior unchanged  # fmt: skip
    assert (
        result == 10
    )  # => still passes -- the refactor changed the CODE, not the CONTRACT
    # => this is TDD's third step in miniature: the test suite (unchanged) is what makes
    # => it safe to rewrite the implementation -- if the refactor broke something, this
    # => exact same assertion would have caught it immediately


def test_clamp_also_handles_the_low_side() -> None:  # => a SECOND case, added during refactor  # fmt: skip
    assert clamp(-5, minimum=0, maximum=10) == 0  # => -5 is below minimum=0, clamps UP to 0  # fmt: skip
    # => confirms the refactored one-liner covers BOTH directions, not just the high side
    # => ex-23/ex-24 exercised directly -- refactoring is also a natural point to add coverage
