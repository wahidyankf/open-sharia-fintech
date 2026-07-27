# pyright: strict
"""Example 64: avgdl Incremental (co-18, co-29)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => from dataclasses: dataclass


@dataclass  # => part of this step's computation, continued from the line above
class RunningAvgdl:  # => part of this step's computation, continued from the line above
    """Tracks avgdl incrementally: O(1) per add, instead of re-scanning every document."""

    total_length: int = 0  # => co-18: sum of every document's length seen so far
    doc_count: int = 0  # => co-29: how many documents contribute to that sum

    def add(
        self, doc_length: int
    ) -> (
        None
    ):  # => fold ONE new document's length into the running totals -- no rescan needed
        """Fold ONE new document's length into the running totals -- no rescan needed."""
        self.total_length += doc_length  # => co-29: O(1) update, not O(N) recomputation
        self.doc_count += (
            1  # => part of this step's computation, continued from the line above
        )

    @property  # => part of this step's computation, continued from the line above
    def avgdl(
        self,
    ) -> (
        float
    ):  # => the current average document length, computed from the running totals
        """The current average document length, computed from the running totals."""
        return (
            self.total_length / self.doc_count if self.doc_count else 0.0
        )  # => co-18: BM25's own avgdl


def recompute_avgdl_from_scratch(
    doc_lengths: list[int],
) -> (
    float
):  # => the reference: recompute avgdl by fully re-scanning every document length
    """The reference: recompute avgdl by fully re-scanning every document length."""
    return (
        sum(doc_lengths) / len(doc_lengths) if doc_lengths else 0.0
    )  # => returns sum(doc_lengths) / len(doc_lengths) if doc_lengths else 0.0


def main() -> None:  # => defines main
    running = RunningAvgdl()  # => co-18: starts with total_length=0, doc_count=0
    doc_lengths: list[int] = [10, 25, 8, 40, 15]  # => 5 documents, added ONE AT A TIME

    for length in (
        doc_lengths
    ):  # => co-29: incremental add, exactly as a live index would receive documents
        running.add(
            length
        )  # => part of this step's computation, continued from the line above
        print(
            f"after adding doc of length {length}: running avgdl={running.avgdl:.4f}"
        )  # => shows after adding doc of length

    from_scratch: float = recompute_avgdl_from_scratch(
        doc_lengths
    )  # => co-18: the reference, recomputed fully
    print(f"final running avgdl:   {running.avgdl:.4f}")  # => shows final running avgdl
    print(f"from-scratch avgdl:    {from_scratch:.4f}")  # => shows from-scratch avgdl

    assert running.avgdl == from_scratch, (
        "the incrementally-maintained avgdl must equal a full recomputation"
    )  # => the incrementally-maintained avgdl must equal a full recomputation
    print(
        f"MATCH: the running avgdl ({running.avgdl:.4f}) exactly equals the from-scratch recomputation ({from_scratch:.4f})"
    )  # => shows MATCH: the running avgdl (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
