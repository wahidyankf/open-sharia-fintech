"""Example 30: pytest verification for A Property Setter That Validates."""

import pytest

from example import Rectangle


def test_negative_width_assignment_raises() -> None:
    r: Rectangle = Rectangle(3.0, 4.0)
    with pytest.raises(
        ValueError
    ):  # => r.width = -1 must raise, not silently accept it
        r.width = -1


# => Run: pytest -- Output: 1 passed
