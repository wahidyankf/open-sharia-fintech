# pyright: strict
"""Example 11: Term Frequency Count (co-12)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def term_frequency(
    tokens: list[str],
) -> dict[
    str, int
]:  # => count how many times each term appears in one document's token list
    """Count how many times each term appears in one document's token list."""
    tf: dict[
        str, int
    ] = {}  # => co-12: term -> raw occurrence count, within THIS one document
    for term in tokens:  # => one token at a time
        tf[term] = tf.get(term, 0) + 1  # => starts at 0 on first sight, then increments
    return tf  # => returns tf


def main() -> None:  # => defines main
    doc_text: str = "search engines index documents so search stays fast for every search"  # => the sample document
    doc_tokens: list[str] = [
        str(t) for t in doc_text.split()
    ]  # => co-06: whitespace tokenization, as in Example 1 (str(t) widens pyright's LiteralString inference to plain str)
    tf: dict[str, int] = term_frequency(
        doc_tokens
    )  # => co-12: this document's own term-frequency table
    for term in sorted(
        tf, key=lambda t: (-tf[t], t)
    ):  # => most frequent first, alphabetical tiebreak
        print(f"{term!r}: tf={tf[term]}")  # => prints this step's result

    assert tf["search"] == 3, (
        "'search' appears 3 times in the sample document"
    )  # => 'search' appears 3 times in the sample document
    assert tf["engines"] == 1, (
        "'engines' appears exactly once"
    )  # => 'engines' appears exactly once
    assert sum(tf.values()) == len(doc_tokens), (
        "tf counts must sum to the total token count"
    )  # => tf counts must sum to the total token count
    print(
        f"MATCH: tf['search']={tf['search']} (repeated term, count > 1) and counts sum to {len(doc_tokens)} tokens"
    )  # => shows MATCH: tf['search']=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
