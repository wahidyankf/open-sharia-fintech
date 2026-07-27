# pyright: strict
"""Example 7: Boolean OR (co-03, co-04)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def boolean_or(
    postings_a: list[int], postings_b: list[int]
) -> list[int]:  # => union two SORTED posting lists -- an OR query (co-03)
    """Union two SORTED posting lists -- an OR query (co-03)."""
    return sorted(
        set(postings_a) | set(postings_b)
    )  # => co-04: set union IS boolean OR


def main() -> None:  # => defines main
    search_postings: list[int] = [1, 3, 5]  # => docs containing "search"
    rank_postings: list[int] = [2, 3, 6]  # => docs containing "rank"
    result: list[int] = boolean_or(
        search_postings, rank_postings
    )  # => docs with EITHER term
    print(f"search postings: {search_postings}")  # => shows search postings
    print(f"rank postings: {rank_postings}")  # => shows rank postings
    print(f"search OR rank: {result}")  # => shows search OR rank

    expected: list[int] = sorted(
        set(search_postings) | set(rank_postings)
    )  # => Python's own set '|'
    assert result == expected, (
        "boolean_or must match Python's native set union"
    )  # => boolean_or must match Python's native set union
    print(
        f"MATCH: boolean_or's result equals Python's set '|' result ({expected})"
    )  # => shows MATCH: boolean_or's result equals Python's set '|' result (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
