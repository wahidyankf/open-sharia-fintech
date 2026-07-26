# pyright: strict
"""Example 5: Posting List Sorted (co-02)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def build_sorted_postings(
    docs: dict[int, list[str]], term: str
) -> list[
    int
]:  # => return term's posting list as a strictly ascending, deduplicated list[int]
    """Return term's posting list as a strictly ascending, deduplicated list[int]."""
    doc_ids: set[int] = {
        doc_id for doc_id, tokens in docs.items() if term in tokens
    }  # => co-02: which docs contain term
    return sorted(
        doc_ids
    )  # => sorted() guarantees ascending order, the standard posting-list invariant


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => doc-ids deliberately inserted OUT of order
        5: ["index", "search"],  # => doc 5's tokens, this fixture's row
        1: ["search", "rank"],  # => doc 1's tokens, this fixture's row
        3: ["search", "documents"],  # => doc 3's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    postings: list[int] = build_sorted_postings(
        docs, "search"
    )  # => co-02: term's own posting list
    print(f"docs inserted in order: {list(docs)}")  # => shows docs inserted in order
    print(f"postings for 'search': {postings}")  # => shows postings for 'search'

    for i in range(1, len(postings)):  # => walks every adjacent pair
        assert postings[i] > postings[i - 1], (
            "postings must be STRICTLY ascending, no ties or drops"
        )  # => postings must be STRICTLY ascending, no ties or drops
    print(
        f"MATCH: postings {postings} are strictly ascending despite docs being inserted as {list(docs)}"
    )  # => shows MATCH: postings


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
