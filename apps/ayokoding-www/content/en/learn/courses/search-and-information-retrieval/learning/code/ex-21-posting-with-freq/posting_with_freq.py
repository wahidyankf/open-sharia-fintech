# pyright: strict
"""Example 21: Posting with Frequency (co-02, co-12)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def build_postings_with_freq(
    docs: dict[int, list[str]], term: str
) -> list[
    tuple[int, int]
]:  # => return term's posting list as (doc_id, tf) tuples, sorted ascending by doc_id
    """Return term's posting list as (doc_id, tf) tuples, sorted ascending by doc_id."""
    postings: list[
        tuple[int, int]
    ] = []  # => co-02: richer than Example 5's bare doc-id list
    for doc_id in sorted(docs):  # => ascending doc_id order, the posting-list invariant
        tf: int = docs[doc_id].count(
            term
        )  # => co-12: how many times term occurs in THIS doc
        if tf > 0:  # => only documents that actually contain the term get a posting
            postings.append((doc_id, tf))  # => records this item, in order
    return postings  # => returns postings


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: [
            "search",
            "search",
            "search",
            "engine",
        ],  # => doc 0's tokens, this fixture's row
        1: ["search", "index"],  # => doc 1's tokens, this fixture's row
        2: ["engine", "engine"],  # => doc 2's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    postings: list[tuple[int, int]] = build_postings_with_freq(
        docs, "search"
    )  # => co-02+co-12: combined
    print(f"postings for 'search': {postings}")  # => shows postings for 'search'

    for doc_id, tf in postings:  # => verifies EVERY tuple, not just one
        raw_count: int = docs[doc_id].count(
            "search"
        )  # => an independent recount, straight from the doc
        assert tf == raw_count, (
            f"doc {doc_id}: posting tf={tf} must match raw count={raw_count}"
        )  # => doc {doc_id}: posting tf={tf} must match raw count={raw_count}
    assert postings == [(0, 3), (1, 1)], (
        "doc 0 has tf=3, doc 1 has tf=1, doc 2 has no 'search' at all"
    )  # => doc 0 has tf=3, doc 1 has tf=1, doc 2 has no 'search' at all
    print(
        "MATCH: every posting's tf equals a raw recount of the term in its own document"
    )  # => shows MATCH: every posting's tf equals a raw recount of the term in its own document


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
