"""Example 48: pytest verification for A Hand-Rolled Some/Nothing With map."""

from typing import Callable

from example import Nothing, Some


def test_map_runs_on_some_and_is_skipped_on_nothing() -> None:
    increment: Callable[[int], int] = lambda x: x + 1
    assert Some(5).map(increment) == Some(6)
    assert Nothing().map(increment) == Nothing()


# => Run: pytest -- Output: 1 passed
