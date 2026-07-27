# pyright: strict
"""Example 60: Incremental Equals Rebuild (co-29)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => from dataclasses: dataclass, field


@dataclass  # => part of this step's computation, continued from the line above
class InvertedIndex:  # => part of this step's computation, continued from the line above
    """A typed, mutable inverted index: term -> {doc_id: term_frequency}."""

    postings: dict[str, dict[int, int]] = field(
        default_factory=lambda: {}
    )  # => postings = field(default_factory=lambda: {})
    doc_lengths: dict[int, int] = field(
        default_factory=lambda: {}
    )  # => doc lengths = field(default_factory=lambda: {})

    def add(
        self, doc_id: int, tokens: list[str]
    ) -> None:  # => index one document's tokens -- updates postings AND doc_lengths
        """Index one document's tokens -- updates postings AND doc_lengths."""
        tf: dict[str, int] = {}  # => starts empty, populated by the loop below
        for t in tokens:  # => iterates one item at a time
            tf[t] = (
                tf.get(t, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
        for term, count in tf.items():  # => iterates one item at a time
            self.postings.setdefault(term, {})[doc_id] = (
                count  # => part of this step's computation, continued from the line above
            )
        self.doc_lengths[doc_id] = len(tokens)  # => self = len(tokens)

    def query(self, term: str) -> set[int]:  # => return every doc-id containing term
        """Return every doc-id containing term."""
        return set(
            self.postings.get(term, {}).keys()
        )  # => returns set(self.postings.get(term, {}).keys())


def build_from_scratch(
    docs: dict[int, list[str]],
) -> (
    InvertedIndex
):  # => a single-pass, from-scratch build -- the reference implementation
    """A single-pass, from-scratch build -- the reference implementation."""
    index = (
        InvertedIndex()
    )  # => co-29: starts empty, exactly like the incremental version did
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        index.add(
            doc_id, tokens
        )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: ["search", "engine", "search"],  # => doc 0's tokens, this fixture's row
        1: ["search", "results"],  # => doc 1's tokens, this fixture's row
        2: ["ranking", "algorithm"],  # => doc 2's tokens, this fixture's row
    }  # => opens/closes this multi-line literal

    incremental = (
        InvertedIndex()
    )  # => co-29: built ONE document at a time, in a different order
    incremental.add(
        2, docs[2]
    )  # => deliberately OUT OF ORDER vs the dict's own iteration order
    incremental.add(
        0, docs[0]
    )  # => part of this step's computation, continued from the line above
    incremental.add(
        1, docs[1]
    )  # => part of this step's computation, continued from the line above

    rebuilt: InvertedIndex = build_from_scratch(
        docs
    )  # => co-29: the from-scratch reference build
    print(
        f"incremental postings['search']: {incremental.postings.get('search')}"
    )  # => shows incremental postings['search']
    print(
        f"rebuilt postings['search']:     {rebuilt.postings.get('search')}"
    )  # => shows rebuilt postings['search']

    all_terms: set[str] = set(incremental.postings) | set(
        rebuilt.postings
    )  # => every term EITHER index knows about
    for term in all_terms:  # => checks EVERY term, not just 'search'
        assert incremental.postings.get(term) == rebuilt.postings.get(term), (
            f"{term!r}: incremental and rebuilt postings must match"
        )  # => {term!r}: incremental and rebuilt postings must match
    assert incremental.doc_lengths == rebuilt.doc_lengths, (
        "doc_lengths must also match between the two builds"
    )  # => doc_lengths must also match between the two builds
    print(
        f"MATCH: incremental (built out of order) and from-scratch rebuild agree on all {len(all_terms)} terms"
    )  # => shows MATCH: incremental (built out of order) and from-scratch rebuild agree on all


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
