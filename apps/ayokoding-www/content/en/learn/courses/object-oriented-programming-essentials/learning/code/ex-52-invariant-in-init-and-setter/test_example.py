"""Example 52: pytest verification for The Same Invariant Enforced in __init__ and a Setter."""

import pytest

from example import Percentage


def test_constructor_path_rejects_out_of_range_value() -> None:
    with pytest.raises(ValueError):
        Percentage(
            150
        )  # => __init__ assigns through the property setter -- same guard fires


def test_setter_path_rejects_out_of_range_value() -> None:
    p: Percentage = Percentage(50)
    with pytest.raises(ValueError):
        p.value = 150  # => neither construction NOR later assignment can violate the invariant


# => Run: pytest -- Output: 2 passed
