"""Example 35: pytest verification for __eq__ Without __hash__ Is Unhashable."""

import pytest

from example import Money


def test_eq_only_class_is_unhashable() -> None:
    with pytest.raises(
        TypeError
    ):  # => hash(Money(...)) must raise, not silently succeed
        {Money(500, "USD")}  # type: ignore  # => set construction calls hash() internally (static checkers correctly flag Money as unhashable)


# => Run: pytest -- Output: 1 passed
