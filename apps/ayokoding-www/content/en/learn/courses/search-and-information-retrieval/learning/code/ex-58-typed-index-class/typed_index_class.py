# pyright: strict
"""Example 58: Typed Index Class (co-01, co-29)."""

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


def main() -> None:  # => defines main
    index = InvertedIndex()  # => co-01: an empty typed index
    index.add(
        0, ["search", "engine", "search"]
    )  # => co-29: co-01's inverted index, built incrementally
    index.add(
        1, ["search", "results"]
    )  # => part of this step's computation, continued from the line above
    index.add(
        2, ["cooking", "recipe"]
    )  # => part of this step's computation, continued from the line above

    search_hits: set[int] = index.query(
        "search"
    )  # => co-01: docs 0 and 1 both contain "search"
    cooking_hits: set[int] = index.query("cooking")  # => only doc 2 contains "cooking"
    print(f"query('search'): {sorted(search_hits)}")  # => shows query('search')
    print(f"query('cooking'): {sorted(cooking_hits)}")  # => shows query('cooking')
    print(f"doc_lengths: {index.doc_lengths}")  # => shows doc_lengths

    assert search_hits == {0, 1}, (
        "'search' must be found in exactly docs 0 and 1"
    )  # => 'search' must be found in exactly docs 0 and 1
    assert cooking_hits == {2}, (
        "'cooking' must be found in exactly doc 2"
    )  # => 'cooking' must be found in exactly doc 2
    assert index.postings["search"][0] == 2, (
        "doc 0's tf for 'search' must be 2, since it appears twice"
    )  # => doc 0's tf for 'search' must be 2, since it appears twice
    assert index.doc_lengths == {0: 3, 1: 2, 2: 2}, (
        "doc_lengths must record each document's own token count"
    )  # => doc_lengths must record each document's own token count
    print(
        "MATCH: the typed InvertedIndex class returns correct doc sets and per-document lengths"
    )  # => shows MATCH: the typed InvertedIndex class returns correct doc sets and per-document lengths


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
