# pyright: strict
"""Example 70: Edge N-Gram Autocomplete (co-33)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def edge_ngrams(
    term: str, min_len: int = 1
) -> list[str]:  # => every PREFIX of term from length min_len up to the full term
    """Every PREFIX of term from length min_len up to the full term."""
    return [
        term[:i] for i in range(min_len, len(term) + 1)
    ]  # => co-33: 's', 'se', 'sea', ..., the full term


def build_edge_ngram_index(
    docs: dict[int, str],
) -> dict[
    str, set[int]
]:  # => index every document's own single term by ALL of its edge n-grams
    """Index every document's own single term by ALL of its edge n-grams."""
    index: dict[
        str, set[int]
    ] = {}  # => co-33: prefix -> {doc-ids whose term starts with this prefix}
    for doc_id, term in docs.items():  # => iterates one item at a time
        for prefix in edge_ngrams(
            term
        ):  # => co-33: EVERY prefix of this document's term gets indexed
            index.setdefault(prefix, set()).add(
                doc_id
            )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def main() -> None:  # => defines main
    docs: dict[int, str] = {
        0: "search",
        1: "season",
        2: "cooking",
    }  # => 3 single-term "documents" (e.g. autocomplete entries)
    index: dict[str, set[int]] = build_edge_ngram_index(
        docs
    )  # => co-33: this vocabulary's own edge n-gram index

    partial_query: str = "sea"  # => a user typing "sea" -- not yet a complete word
    hits: set[int] = index.get(
        partial_query, set()
    )  # => co-33: everything whose FULL term starts with "sea"
    print(
        f"edge n-grams of 'search': {edge_ngrams('search')}"
    )  # => shows edge n-grams of 'search'
    print(f"query {partial_query!r} matches docs: {sorted(hits)}")  # => shows query

    assert hits == {0, 1}, (
        "'sea' must match BOTH 'search' (doc 0) and 'season' (doc 1) -- both start with it"
    )  # => 'sea' must match BOTH 'search' (doc 0) and 'season' (doc 1) -- both start with it
    assert 2 not in hits, (
        "'cooking' (doc 2) must NOT match -- it does not start with 'sea'"
    )  # => 'cooking' (doc 2) must NOT match -- it does not start with 'sea'
    print(
        f"MATCH: typing 'sea' retrieves both prefix-matching terms, correctly excluding the unrelated one"
    )  # => shows MATCH: typing 'sea' retrieves both prefix-matching terms, correctly excluding the unrelated one


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
