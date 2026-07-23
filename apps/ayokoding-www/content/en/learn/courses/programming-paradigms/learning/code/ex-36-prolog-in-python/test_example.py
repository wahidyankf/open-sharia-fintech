"""Example 36: pytest verification for Prolog-in-Python (Unification + Backtracking)."""

from example import grandparent


def test_grandparent_query_resolves_via_search() -> None:
    assert list(grandparent("alice")) == ["carol"]  # => same answer as example 19's comprehension version


def test_a_person_with_no_grandchildren_yields_nothing() -> None:
    assert list(grandparent("dave")) == []  # => dave has no recorded children at all -- search finds none


# => Run: pytest -- Output: 2 passed
