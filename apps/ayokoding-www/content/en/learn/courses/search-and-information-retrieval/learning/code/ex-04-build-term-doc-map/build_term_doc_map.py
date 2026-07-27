# pyright: strict
"""Example 4: Build Term-Doc Map (co-01)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def build_term_doc_map(
    docs: dict[int, list[str]],
) -> dict[
    str, set[int]
]:  # => build a term -> set-of-doc-ids inverted index over already-tokenized docs
    """Build a term -> set-of-doc-ids inverted index over already-tokenized docs."""
    index: dict[
        str, set[int]
    ] = {}  # => co-01: the inverted index -- empty until populated
    for doc_id, tokens in docs.items():  # => one document at a time
        for term in tokens:  # => one term at a time, within this document
            index.setdefault(term, set()).add(
                doc_id
            )  # => creates the term's set on first sight, adds doc_id
    return index  # => returns index


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => 3 tiny, already-tokenized documents
        0: [
            "search",
            "engines",
            "rank",
            "documents",
        ],  # => doc 0's tokens, this fixture's row
        1: [
            "search",
            "index",
            "documents",
            "fast",
        ],  # => doc 1's tokens, this fixture's row
        2: [
            "rank",
            "pages",
            "by",
            "relevance",
        ],  # => doc 2's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    index: dict[str, set[int]] = build_term_doc_map(
        docs
    )  # => co-01: term -> {doc-ids containing it}
    for term in sorted(index):  # => sorted for deterministic, readable output
        print(f"{term!r}: {sorted(index[term])}")  # => prints this step's result

    assert index["search"] == {0, 1}, (
        "'search' must map to exactly docs 0 and 1"
    )  # => 'search' must map to exactly docs 0 and 1
    assert index["rank"] == {0, 2}, (
        "'rank' must map to exactly docs 0 and 2"
    )  # => 'rank' must map to exactly docs 0 and 2
    for (
        term,
        doc_ids,
    ) in index.items():  # => a general check across every term, not just the two above
        for doc_id in doc_ids:  # => every doc-id this term claims to appear in
            assert term in docs[doc_id], (
                f"{term!r} claims doc {doc_id} but is absent from it"
            )  # => {term!r} claims doc {doc_id} but is absent from it
    print(
        "MATCH: every term maps to exactly the docs that actually contain it"
    )  # => shows MATCH: every term maps to exactly the docs that actually contain it


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
