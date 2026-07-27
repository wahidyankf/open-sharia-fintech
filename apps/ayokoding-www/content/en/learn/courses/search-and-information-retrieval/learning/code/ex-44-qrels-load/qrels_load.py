# pyright: strict
"""Example 44: Qrels Load (co-23)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def load_qrels(
    raw: list[tuple[str, int]],
) -> dict[
    str, set[int]
]:  # => load a flat list of (query, relevant_doc_id) rows into query -> {relevant doc-ids}
    """Load a flat list of (query, relevant_doc_id) rows into query -> {relevant doc-ids}."""
    qrels: dict[str, set[int]] = {}  # => co-23: the ground-truth relevance judgments
    for query, doc_id in raw:  # => one labeled (query, doc) judgment at a time
        qrels.setdefault(query, set()).add(
            doc_id
        )  # => part of this step's computation, continued from the line above
    return qrels  # => returns qrels


def main() -> None:  # => defines main
    raw_judgments: list[
        tuple[str, int]
    ] = [  # => flat rows, as a human annotator might produce them
        (
            "search engine",
            1,
        ),  # => part of this step's computation, continued from the line above
        (
            "search engine",
            3,
        ),  # => part of this step's computation, continued from the line above
        (
            "search engine",
            7,
        ),  # => part of this step's computation, continued from the line above
        (
            "ranking algorithm",
            2,
        ),  # => part of this step's computation, continued from the line above
        (
            "ranking algorithm",
            4,
        ),  # => part of this step's computation, continued from the line above
    ]  # => opens/closes this multi-line literal
    qrels: dict[str, set[int]] = load_qrels(
        raw_judgments
    )  # => co-23: the loaded, query-grouped judgments
    for query in sorted(qrels):  # => iterates one item at a time
        print(f"{query!r}: {sorted(qrels[query])}")  # => prints this step's result

    assert qrels["search engine"] == {1, 3, 7}, (
        "'search engine' must map to exactly its 3 labeled relevant docs"
    )  # => 'search engine' must map to exactly its 3 labeled relevant docs
    assert qrels["ranking algorithm"] == {2, 4}, (
        "'ranking algorithm' must map to exactly its 2 labeled relevant docs"
    )  # => 'ranking algorithm' must map to exactly its 2 labeled relevant docs
    assert len(qrels) == 2, (
        "there must be exactly 2 distinct queries in this judgment set"
    )  # => there must be exactly 2 distinct queries in this judgment set
    print(
        f"MATCH: each query maps to exactly its labeled relevant docs, {len(qrels)} distinct queries total"
    )  # => shows MATCH: each query maps to exactly its labeled relevant docs,


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
