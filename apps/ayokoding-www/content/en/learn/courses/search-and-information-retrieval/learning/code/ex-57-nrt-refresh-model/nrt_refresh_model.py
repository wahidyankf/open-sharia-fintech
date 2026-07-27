# pyright: strict
"""Example 57: NRT Refresh Model (co-27)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => from dataclasses: dataclass, field


@dataclass  # => part of this step's computation, continued from the line above
class NrtIndex:  # => part of this step's computation, continued from the line above
    """Docs added via add() sit in a PENDING buffer until refresh() commits them."""

    committed: dict[int, list[str]] = field(
        default_factory=lambda: {}
    )  # => co-27: SEARCHABLE documents
    pending: dict[int, list[str]] = field(
        default_factory=lambda: {}
    )  # => co-27: buffered, NOT yet searchable

    def add(
        self, doc_id: int, tokens: list[str]
    ) -> None:  # => buffer a document -- it is NOT searchable until refresh() runs
        """Buffer a document -- it is NOT searchable until refresh() runs."""
        self.pending[doc_id] = (
            tokens  # => co-27: goes into the buffer, not the committed index
        )

    def refresh(self) -> None:  # => commit every pending document, making it searchable
        """Commit every pending document, making it searchable."""
        for (
            doc_id,
            tokens,
        ) in self.pending.items():  # => co-27: moves EVERY buffered doc into committed
            self.committed[doc_id] = tokens  # => self = tokens
        self.pending.clear()  # => the buffer is now empty -- everything has been committed

    def contains(
        self, doc_id: int
    ) -> bool:  # => true only if doc_id is in the COMMITTED (searchable) index
        """True only if doc_id is in the COMMITTED (searchable) index."""
        return (
            doc_id in self.committed
        )  # => co-27: pending docs do NOT count as findable


def main() -> None:  # => defines main
    index = NrtIndex()  # => co-27: starts with nothing committed, nothing pending
    index.add(1, ["search", "engine"])  # => buffered -- NOT yet searchable
    print(
        f"immediately after add(1, ...): contains(1)={index.contains(1)}"
    )  # => shows immediately after add(1, ...): contains(1)=

    assert not index.contains(1), (
        "a document must be INVISIBLE to search before refresh() runs"
    )  # => a document must be INVISIBLE to search before refresh() runs

    index.refresh()  # => co-27: commits the pending buffer
    print(
        f"after refresh(): contains(1)={index.contains(1)}"
    )  # => shows after refresh(): contains(1)=
    assert index.contains(1), (
        "the SAME document must be VISIBLE immediately after refresh()"
    )  # => the SAME document must be VISIBLE immediately after refresh()
    print(
        "MATCH: doc 1 was invisible pre-refresh and visible post-refresh -- genuine NRT behavior"
    )  # => shows MATCH: doc 1 was invisible pre-refresh and visible post-refresh -- genuine NRT behavior


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
