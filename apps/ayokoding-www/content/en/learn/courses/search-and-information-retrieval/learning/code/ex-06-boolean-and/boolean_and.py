# pyright: strict
"""Example 6: Boolean AND (co-03, co-04)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def boolean_and(
    postings_a: list[int], postings_b: list[int]
) -> list[int]:  # => intersect two SORTED posting lists -- an AND query (co-03)
    """Intersect two SORTED posting lists -- an AND query (co-03)."""
    return sorted(
        set(postings_a) & set(postings_b)
    )  # => co-04: set intersection IS boolean AND


def main() -> None:  # => defines main
    search_postings: list[int] = [1, 3, 5, 7, 9]  # => docs containing "search"
    engine_postings: list[int] = [2, 3, 5, 8, 9]  # => docs containing "engine"
    result: list[int] = boolean_and(
        search_postings, engine_postings
    )  # => docs with BOTH terms
    print(f"search postings: {search_postings}")  # => shows search postings
    print(f"engine postings: {engine_postings}")  # => shows engine postings
    print(f"search AND engine: {result}")  # => shows search AND engine

    expected: list[int] = sorted(
        set(search_postings) & set(engine_postings)
    )  # => Python's own set '&'
    assert result == expected, (
        "boolean_and must match Python's native set intersection"
    )  # => boolean_and must match Python's native set intersection
    print(
        f"MATCH: boolean_and's result equals Python's set '&' result ({expected})"
    )  # => shows MATCH: boolean_and's result equals Python's set '&' result (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
