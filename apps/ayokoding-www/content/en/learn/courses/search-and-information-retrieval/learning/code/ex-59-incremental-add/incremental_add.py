# pyright: strict
"""Example 59: Incremental Add (co-29)."""

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
    index = (
        InvertedIndex()
    )  # => co-01: an already "built" index, before the new document arrives
    index.add(
        0, ["search", "engine"]
    )  # => part of this step's computation, continued from the line above
    index.add(
        1, ["cooking", "recipe"]
    )  # => part of this step's computation, continued from the line above

    before: set[int] = index.query("ranking")  # => co-29: the term does not exist YET
    print(
        f"query('ranking') before incremental add: {sorted(before)}"
    )  # => shows query('ranking') before incremental add
    assert before == set(), (
        "'ranking' must be unfindable before any document containing it is added"
    )  # => 'ranking' must be unfindable before any document containing it is added

    index.add(
        2, ["ranking", "algorithm"]
    )  # => co-29: incremental add -- NO rebuild of docs 0 or 1
    after: set[int] = index.query(
        "ranking"
    )  # => co-29: the SAME index object, queried again
    print(
        f"query('ranking') after incremental add: {sorted(after)}"
    )  # => shows query('ranking') after incremental add

    assert after == {2}, (
        "'ranking' must be immediately findable in the newly added doc 2"
    )  # => 'ranking' must be immediately findable in the newly added doc 2
    assert index.query("search") == {0}, (
        "doc 0's postings must be UNCHANGED by the incremental add"
    )  # => doc 0's postings must be UNCHANGED by the incremental add
    print(
        "MATCH: doc 2 became findable immediately, and the pre-existing postings were untouched"
    )  # => shows MATCH: doc 2 became findable immediately, and the pre-existing postings were untouched


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
