"""Example 25: pytest verification for __post_init__ Validation."""

import pytest

from example import Temperature


def test_valid_temperature_constructs() -> None:
    assert Temperature(20.0).celsius == 20.0


def test_below_absolute_zero_raises_value_error() -> None:
    with pytest.raises(
        ValueError
    ):  # => __post_init__ raises before construction completes
        Temperature(-300.0)  # => colder than physically possible


# => Run: pytest -- Output: 2 passed
