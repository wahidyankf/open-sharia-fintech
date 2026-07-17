"""Example 5: pytest verification for A Frozen Dataclass Rejects Mutation."""

from dataclasses import FrozenInstanceError

from example import Point


def test_frozen_dataclass_rejects_assignment() -> None:
    p = Point(1, 2)
    try:
        p.x = 99  # type: ignore[misc]  # => frozen dataclasses block ALL later assignment
        raised = False
    except FrozenInstanceError:
        raised = True
    assert raised is True
    assert p == Point(1, 2)  # => unchanged -- the assignment never took effect


# => Run: pytest -- Output: 1 passed
