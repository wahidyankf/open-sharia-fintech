# pyright: strict
"""Example 16: Stop-Word Recall Risk (co-08, co-11)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

STOP_WORDS: frozenset[str] = frozenset(
    {"the", "a", "an", "of", "in", "on", "and", "or", "to", "is", "are", "for"}
)  # => STOP WORDS = frozenset({"the", "a", "an", "of", "in", "on", ...


def build_index(
    docs: dict[int, list[str]], *, drop_stop_words: bool
) -> dict[
    str, set[int]
]:  # => build a term -> doc-id-set index, optionally dropping stop words first
    """Build a term -> doc-id-set index, optionally dropping stop words first."""
    index: dict[str, set[int]] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        kept: list[str] = [
            t for t in tokens if not (drop_stop_words and t in STOP_WORDS)
        ]  # => co-08: the filter, if enabled
        for term in kept:  # => iterates one item at a time
            index.setdefault(term, set()).add(
                doc_id
            )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def query_and(
    index: dict[str, set[int]], terms: list[str]
) -> set[
    int
]:  # => a boolean AND query -- terms absent from the index contribute an empty set
    """A boolean AND query -- terms absent from the index contribute an empty set."""
    result: set[int] | None = None  # => result = None
    for term in terms:  # => iterates one item at a time
        postings: set[int] = index.get(
            term, set()
        )  # => co-11: a stop word never indexed returns EMPTY
        result = (
            postings if result is None else result & postings
        )  # => result = postings if result is None else result & postings
    return result or set()  # => returns result or set()


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {
        0: ["to", "be", "or", "not", "to", "be"],
        1: ["the", "answer", "is", "42"],
    }  # => docs = {0: ["to", "be", "or", "not", "to", "be"], 1: [...
    stripped_index: dict[str, set[int]] = build_index(
        docs, drop_stop_words=True
    )  # => co-08: stop words dropped
    full_index: dict[str, set[int]] = build_index(
        docs, drop_stop_words=False
    )  # => a baseline WITHOUT the filter

    stripped_hits: set[int] = query_and(
        stripped_index, ["to", "be", "or"]
    )  # => a phrase of ONLY stop words
    full_hits: set[int] = query_and(
        full_index, ["to", "be", "or"]
    )  # => the SAME phrase, unstripped index
    print(
        f"query ['to', 'be', 'or'] against STRIPPED index: {sorted(stripped_hits)}"
    )  # => shows query ['to', 'be', 'or'] against STRIPPED index
    print(
        f"query ['to', 'be', 'or'] against FULL index:     {sorted(full_hits)}"
    )  # => shows query ['to', 'be', 'or'] against FULL index

    assert stripped_hits == set(), (
        "the stripped index must return NOTHING for an all-stop-word query"
    )  # => the stripped index must return NOTHING for an all-stop-word query
    assert full_hits == {0}, (
        "the unstripped index must still find doc 0, 'To be or not to be'"
    )  # => the unstripped index must still find doc 0, 'To be or not to be'
    print(
        "MATCH: the stripped index returns empty (recall lost) where the unstripped index correctly finds doc 0"
    )  # => shows MATCH: the stripped index returns empty (recall lost) where the unstripped index correctly finds doc 0


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
