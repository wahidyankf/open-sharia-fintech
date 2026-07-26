# pyright: strict
"""Example 12: Document Frequency (co-13)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def document_frequency(
    docs: dict[int, list[str]],
) -> dict[str, int]:  # => count, per term, how many documents contain it at least once
    """Count, per term, how many documents contain it at least once."""
    df: dict[
        str, int
    ] = {}  # => co-13: term -> number of DOCUMENTS (not occurrences) containing it
    for tokens in docs.values():  # => one document's token list at a time
        for term in set(
            tokens
        ):  # => set() -- a term counts ONCE per document, however often it repeats
            df[term] = (
                df.get(term, 0) + 1
            )  # => counter pattern: 0 on first sight, then increments
    return df  # => returns df


def main() -> None:  # => defines main
    docs: dict[
        int, list[str]
    ] = {  # => "search" appears in every doc; "engine" only in doc 0
        0: [
            "search",
            "engine",
            "search",
            "ranks",
        ],  # => "search" repeats but still counts once for df
        1: ["search", "index", "documents"],  # => doc 1's tokens, this fixture's row
        2: ["search", "fast", "results"],  # => doc 2's tokens, this fixture's row
    }  # => opens/closes this multi-line literal
    n_docs: int = len(docs)  # => N, the total corpus size
    df: dict[str, int] = document_frequency(
        docs
    )  # => co-13: this corpus's own document-frequency table
    for term in sorted(df):  # => iterates one item at a time
        print(f"{term!r}: df={df[term]} of N={n_docs}")  # => prints this step's result

    assert df["search"] == n_docs, (
        "'search' appears in EVERY doc, so its df must equal N"
    )  # => 'search' appears in EVERY doc, so its df must equal N
    assert df["engine"] == 1, (
        "'engine' appears in exactly one document"
    )  # => 'engine' appears in exactly one document
    print(
        f"MATCH: df['search']={df['search']} equals N={n_docs} (present in every doc)"
    )  # => shows MATCH: df['search']=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
