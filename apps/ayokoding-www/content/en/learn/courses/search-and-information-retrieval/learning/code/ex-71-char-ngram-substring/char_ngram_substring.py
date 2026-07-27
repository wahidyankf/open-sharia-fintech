# pyright: strict
"""Example 71: Char N-Gram Substring (co-33)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def char_ngrams(
    term: str, n: int = 3
) -> list[
    str
]:  # => every contiguous n-character substring of term -- covers the WHOLE word, not just its start
    """Every contiguous n-character substring of term -- covers the WHOLE word, not just its start."""
    if len(term) < n:  # => true when len(term) < n
        return [
            term
        ]  # => co-33: too short for a full n-gram -- the whole term is its own single gram
    return [
        term[i : i + n] for i in range(len(term) - n + 1)
    ]  # => co-33: sliding window of width n


def build_char_ngram_index(
    docs: dict[int, str], n: int = 3
) -> dict[str, set[int]]:  # => defines build char ngram index
    index: dict[
        str, set[int]
    ] = {}  # => co-33: n-gram -> {doc-ids whose term contains this n-gram}
    for doc_id, term in docs.items():  # => iterates one item at a time
        for gram in char_ngrams(
            term, n
        ):  # => co-33: EVERY trigram of this document's term
            index.setdefault(gram, set()).add(
                doc_id
            )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def main() -> None:  # => defines main
    docs: dict[int, str] = {
        0: "search",
        1: "research",
        2: "cooking",
    }  # => "arch" is INTERIOR to both 0 and 1
    index: dict[str, set[int]] = build_char_ngram_index(
        docs, n=3
    )  # => co-33: this vocabulary's own trigram index

    interior_query: str = "arch"  # => co-33: appears in the MIDDLE of "search" and "research", not at the start
    query_grams: list[str] = char_ngrams(
        interior_query, n=3
    )  # => co-33: 'arc', 'rch' -- trigrams of the query itself
    hits: set[int] = set[int]().union(
        *(index.get(g, set()) for g in query_grams)
    )  # => co-33: docs matching ANY query trigram
    print(
        f"trigrams of 'search': {char_ngrams('search', n=3)}"
    )  # => shows trigrams of 'search'
    print(
        f"trigrams of query 'arch': {query_grams}"
    )  # => shows trigrams of query 'arch'
    print(
        f"interior substring query {interior_query!r} matches docs: {sorted(hits)}"
    )  # => shows interior substring query

    assert 0 in hits and 1 in hits, (
        "'arch' is an INTERIOR substring of both 'search' and 'research' -- both must match"
    )  # => 'arch' is an INTERIOR substring of both 'search' and 'research' -- both must match
    assert 2 not in hits, (
        "'cooking' contains no trigram of 'arch' -- it must NOT match"
    )  # => 'cooking' contains no trigram of 'arch' -- it must NOT match
    print(
        f"MATCH: an interior substring query found both containing documents via shared character n-grams"
    )  # => shows MATCH: an interior substring query found both containing documents via shared character n-grams


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
