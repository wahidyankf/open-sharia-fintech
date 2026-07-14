"""Example 37: pytest verification for A Frozen Dataclass Is Hashable by Default."""

from example import Point


def test_frozen_dataclass_works_as_dict_key() -> None:
    lookup: dict[Point, str] = {Point(1, 2): "origin-ish"}
    assert (
        lookup[Point(1, 2)] == "origin-ish"
    )  # => a NEW, equal Point finds the same entry


def test_frozen_dataclass_deduplicates_in_a_set() -> None:
    members: set[Point] = {Point(1, 2), Point(1, 2)}
    assert len(members) == 1


# => Run: pytest -- Output: 2 passed
