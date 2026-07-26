# pyright: strict
"""Example 56: Segment Merge Model (co-27)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def build_index(
    docs: dict[int, list[str]],
) -> dict[
    str, set[int]
]:  # => build a term -> doc-id-set index over the given documents -- one immutable segment
    """Build a term -> doc-id-set index over the given documents -- one immutable segment."""
    index: dict[str, set[int]] = {}  # => starts empty, populated by the loop below
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        for term in tokens:  # => iterates one item at a time
            index.setdefault(term, set()).add(
                doc_id
            )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def merge_segments(
    segment_a: dict[str, set[int]], segment_b: dict[str, set[int]]
) -> dict[
    str, set[int]
]:  # => merge two immutable per-segment indexes into one combined index -- co-27's own segment model
    """Merge two immutable per-segment indexes into one combined index -- co-27's own segment model."""
    merged: dict[str, set[int]] = {
        term: set(doc_ids) for term, doc_ids in segment_a.items()
    }  # => copies segment A's postings first
    for (
        term,
        doc_ids,
    ) in (
        segment_b.items()
    ):  # => co-27: folds segment B's postings in, union-ing where terms overlap
        merged.setdefault(term, set()).update(
            doc_ids
        )  # => part of this step's computation, continued from the line above
    return merged  # => returns merged


def main() -> None:  # => defines main
    docs_segment1: dict[int, list[str]] = {
        0: ["search", "engine"],
        1: ["search", "index"],
        2: ["fast", "ranking"],
    }  # => an EARLIER write batch
    docs_segment2: dict[int, list[str]] = {
        3: ["search", "results"],
        4: ["engine", "speed"],
        5: ["index", "structure"],
    }  # => a LATER write batch

    segment1: dict[str, set[int]] = build_index(
        docs_segment1
    )  # => co-27: the first immutable segment, docs 0-2
    segment2: dict[str, set[int]] = build_index(
        docs_segment2
    )  # => co-27: the second immutable segment, docs 3-5
    merged: dict[str, set[int]] = merge_segments(
        segment1, segment2
    )  # => co-27: the two segments, merged into one
    print(
        f"segment 1 ('search'): {sorted(segment1.get('search', set()))}"
    )  # => shows segment 1 ('search')
    print(
        f"segment 2 ('search'): {sorted(segment2.get('search', set()))}"
    )  # => shows segment 2 ('search')
    print(
        f"merged    ('search'): {sorted(merged.get('search', set()))}"
    )  # => shows merged    ('search')

    all_docs: dict[int, list[str]] = {
        **docs_segment1,
        **docs_segment2,
    }  # => the SAME documents, built as ONE segment from scratch
    single_segment: dict[str, set[int]] = build_index(
        all_docs
    )  # => the reference: a from-scratch, single-segment build

    for term in single_segment:  # => checks EVERY term, not just "search"
        assert merged.get(term, set()) == single_segment[term], (
            f"{term!r}: merged postings must match the single-segment build"
        )  # => {term!r}: merged postings must match the single-segment build
    print(
        f"MATCH: the merged 2-segment index answers every term identically to a from-scratch single-segment build"
    )  # => shows MATCH: the merged 2-segment index answers every term identically to a from-scratch single-segment build


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
