# pyright: strict
"""Example 54: Phrase Query (co-28)."""

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


def phrase_query(
    index: dict[str, dict[int, list[int]]], term1: str, term2: str
) -> set[
    int
]:  # => return doc-ids where term2 occurs at EXACTLY one position after term1 -- an adjacent phrase
    """Return doc-ids where term2 occurs at EXACTLY one position after term1 -- an adjacent phrase."""
    hits: set[int] = (
        set()
    )  # => co-28: documents where the exact phrase "term1 term2" appears
    docs_with_both: set[int] = set(index.get(term1, {})) & set(
        index.get(term2, {})
    )  # => co-04: must contain BOTH terms first
    for doc_id in docs_with_both:  # => iterates one item at a time
        positions1: set[int] = set(
            index[term1][doc_id]
        )  # => every position term1 occurs at, in this doc
        positions2: set[int] = set(
            index[term2][doc_id]
        )  # => every position term2 occurs at, in this doc
        if any(
            (p + 1) in positions2 for p in positions1
        ):  # => co-28: ADJACENT -- term2 right after term1
            hits.add(
                doc_id
            )  # => part of this step's computation, continued from the line above
    return hits  # => returns hits


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: [
            "the",
            "quick",
            "brown",
            "fox",
        ],  # => "quick brown" ARE adjacent -- a phrase match
        1: [
            "the",
            "brown",
            "quick",
            "fox",
        ],  # => both words present, but NOT adjacent (reversed) -- no match
        2: [
            "a",
            "very",
            "quick",
            "and",
            "very",
            "brown",
            "animal",
        ],  # => both present, far apart -- no match
    }  # => opens/closes this multi-line literal
    index: dict[str, dict[int, list[int]]] = build_positional_index(
        docs
    )  # => co-28: this corpus's own positional index
    hits: set[int] = phrase_query(
        index, "quick", "brown"
    )  # => co-28: the phrase query "quick brown"
    print(
        f"phrase 'quick brown' matches docs: {sorted(hits)}"
    )  # => shows phrase 'quick brown' matches docs

    assert hits == {0}, (
        "only doc 0 has 'quick' immediately followed by 'brown'"
    )  # => only doc 0 has 'quick' immediately followed by 'brown'
    print(
        f"MATCH: exactly doc 0 matches the phrase -- docs 1 and 2 contain both words but not adjacently"
    )  # => shows MATCH: exactly doc 0 matches the phrase -- docs 1 and 2 contain both words but not adjacently


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
