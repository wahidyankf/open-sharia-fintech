"""Example 70: A Well-Tested Function -- Run mutmut, Read the Surviving-Mutant Report."""
# Both tests below look thorough, and coverage.py would call this function 100% covered --
# but neither one probes the boundary age == 18, which is exactly what mutmut exposes below.

from adult import is_adult  # => co-22: the ONE function every mutant below mutates  # fmt: skip


def test_is_adult_true() -> None:  # => co-22: looks thorough -- passes for a clearly-adult age  # fmt: skip
    assert is_adult(20) is True  # => a genuinely adult age, far from the boundary  # fmt: skip


def test_is_adult_false() -> None:  # => co-22: and for a clearly-not-adult age  # fmt: skip
    assert is_adult(10) is False  # => a genuinely non-adult age, far from the boundary  # fmt: skip
    # => NEITHER test probes the boundary (age == 18) -- that gap is what mutmut exposes below
