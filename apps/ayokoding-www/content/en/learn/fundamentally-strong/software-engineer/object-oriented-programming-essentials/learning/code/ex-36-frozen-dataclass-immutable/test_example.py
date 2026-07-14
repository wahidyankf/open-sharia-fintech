"""Example 36: pytest verification for A Frozen Dataclass Rejects Field Assignment."""

import dataclasses

import pytest

from example import Point


def test_assigning_frozen_field_raises_frozen_instance_error() -> None:
    p: Point = Point(1, 2)
    with pytest.raises(
        dataclasses.FrozenInstanceError
    ):  # => the exact documented exception type
        p.x = 99  # type: ignore  # => static checkers also flag frozen-field assignment as an error


# => Run: pytest -- Output: 1 passed
