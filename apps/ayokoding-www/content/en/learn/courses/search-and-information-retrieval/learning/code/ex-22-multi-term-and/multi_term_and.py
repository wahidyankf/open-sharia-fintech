# pyright: strict
"""Example 22: Multi-Term AND (co-04)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def intersect(
    a: list[int], b: list[int]
) -> list[int]:  # => two-list sorted intersection, the same primitive Example 6 used
    """Two-list sorted intersection, the same primitive Example 6 used."""
    return sorted(set(a) & set(b))  # => returns sorted(set(a) & set(b))


def multi_term_and(
    posting_lists: list[list[int]],
) -> list[
    int
]:  # => aND together an arbitrary number of posting lists by chaining pairwise intersections
    """AND together an arbitrary number of posting lists by chaining pairwise intersections."""
    if (
        not posting_lists
    ):  # => an AND with zero terms is undefined -- guard it explicitly
        return []  # => returns []
    result: list[int] = posting_lists[0]  # => start from the FIRST list
    for postings in posting_lists[1:]:  # => fold in one MORE list at a time
        result = intersect(
            result, postings
        )  # => co-04: (result AND postings), chained left to right
    return result  # => returns result


def main() -> None:  # => defines main
    search_postings: list[int] = [1, 2, 3, 4, 5, 6]  # => docs with "search"
    engine_postings: list[int] = [2, 3, 5, 6, 8]  # => docs with "engine"
    fast_postings: list[int] = [3, 5, 6, 9]  # => docs with "fast"
    chained: list[int] = multi_term_and(
        [search_postings, engine_postings, fast_postings]
    )  # => co-04: 3-way AND
    print(
        f"search AND engine AND fast: {chained}"
    )  # => shows search AND engine AND fast

    expected: list[int] = sorted(
        set(search_postings) & set(engine_postings) & set(fast_postings)
    )  # => all 3 sets at once
    assert chained == expected, (
        "the chained pairwise AND must equal the simultaneous 3-set intersection"
    )  # => the chained pairwise AND must equal the simultaneous 3-set intersection
    print(
        f"MATCH: chained result {chained} equals the full 3-set intersection {expected}"
    )  # => shows MATCH: chained result


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
