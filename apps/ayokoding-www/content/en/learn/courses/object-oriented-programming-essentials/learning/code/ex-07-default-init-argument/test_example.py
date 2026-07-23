"""Example 7: pytest verification for A Default __init__ Argument."""

from example import Dog


def test_default_legs_applies_when_omitted() -> None:
    assert (
        Dog("Rex").legs == 4
    )  # => no legs= argument supplied, so the default (4) is used


def test_explicit_legs_overrides_default() -> None:
    assert (
        Dog("Tripod", legs=3).legs == 3
    )  # => an explicit argument overrides the default


# => Run: pytest -- Output: 2 passed
