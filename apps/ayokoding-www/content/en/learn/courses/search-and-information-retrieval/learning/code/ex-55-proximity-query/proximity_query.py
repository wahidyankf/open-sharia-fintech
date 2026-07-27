# pyright: strict
"""Example 55: Proximity Query (co-28)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def build_positional_index(
    docs: dict[int, list[str]],
) -> dict[str, dict[int, list[int]]]:  # => defines build positional index
    index: dict[
        str, dict[int, list[int]]
    ] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        for position, term in enumerate(tokens):  # => iterates one item at a time
            index.setdefault(term, {}).setdefault(doc_id, []).append(
                position
            )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def proximity_query(
    index: dict[str, dict[int, list[int]]], term1: str, term2: str, max_distance: int
) -> set[
    int
]:  # => return doc-ids where term1 and term2 occur within max_distance positions of each other
    """Return doc-ids where term1 and term2 occur within max_distance positions of each other."""
    hits: set[int] = (
        set()
    )  # => co-28: documents where the two terms are CLOSE, not necessarily adjacent
    docs_with_both: set[int] = set(index.get(term1, {})) & set(
        index.get(term2, {})
    )  # => docs with both = set(index.get(term1, {})) & set(index.get(term2...
    for doc_id in docs_with_both:  # => iterates one item at a time
        positions1: list[int] = index[term1][
            doc_id
        ]  # => positions1 = index[term1][doc_id]
        positions2: list[int] = index[term2][
            doc_id
        ]  # => positions2 = index[term2][doc_id]
        if any(
            abs(p1 - p2) <= max_distance for p1 in positions1 for p2 in positions2
        ):  # => co-28: WITHIN N, either direction
            hits.add(
                doc_id
            )  # => part of this step's computation, continued from the line above
    return hits  # => returns hits


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: [
            "search",
            "a",
            "b",
            "engine",
        ],  # => "search" at 0, "engine" at 3 -- distance 3
        1: [
            "search",
            "a",
            "b",
            "c",
            "d",
            "engine",
        ],  # => "search" at 0, "engine" at 5 -- distance 5
    }  # => opens/closes this multi-line literal
    index: dict[str, dict[int, list[int]]] = build_positional_index(
        docs
    )  # => co-28: this corpus's own positional index
    max_distance: int = 3  # => N=3: terms within 3 positions of each other count

    hits: set[int] = proximity_query(
        index, "search", "engine", max_distance
    )  # => co-28: the proximity query
    print(
        f"proximity('search', 'engine', N={max_distance}) matches: {sorted(hits)}"
    )  # => shows proximity('search', 'engine', N=

    assert 0 in hits, (
        "doc 0 has 'search' and 'engine' exactly 3 apart -- within N=3, must match"
    )  # => doc 0 has 'search' and 'engine' exactly 3 apart -- within N=3, must match
    assert 1 not in hits, (
        "doc 1 has 'search' and 'engine' 5 apart -- N+2 beyond N=3, must be excluded"
    )  # => doc 1 has 'search' and 'engine' 5 apart -- N+2 beyond N=3, must be excluded
    print(
        f"MATCH: doc 0 (distance 3, within N={max_distance}) matches; doc 1 (distance 5, beyond N) is excluded"
    )  # => shows MATCH: doc 0 (distance 3, within N=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
