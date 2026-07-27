# pyright: strict
"""Example 53: Positional Index Build (co-28)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def build_positional_index(
    docs: dict[int, list[str]],
) -> dict[
    str, dict[int, list[int]]
]:  # => build term -> doc_id -> [positions] -- a richer posting than Example 21's bare tf count
    """Build term -> doc_id -> [positions] -- a richer posting than Example 21's bare tf count."""
    index: dict[
        str, dict[int, list[int]]
    ] = {}  # => co-28: the positional index -- nested by term, then doc
    for doc_id, tokens in docs.items():  # => iterates one item at a time
        for position, term in enumerate(
            tokens
        ):  # => co-28: position is the 0-based offset WITHIN this document
            index.setdefault(term, {}).setdefault(doc_id, []).append(
                position
            )  # => part of this step's computation, continued from the line above
    return index  # => returns index


def main() -> None:  # => defines main
    docs: dict[int, list[str]] = {  # => docs = {
        0: [
            "the",
            "quick",
            "brown",
            "fox",
            "jumps",
            "over",
            "the",
            "lazy",
            "dog",
        ],  # => "the" appears TWICE, at 0 and 6
    }  # => opens/closes this multi-line literal
    index: dict[str, dict[int, list[int]]] = build_positional_index(
        docs
    )  # => co-28: this doc's own positional index
    print(
        f"positions of 'the' in doc 0: {index['the'][0]}"
    )  # => shows positions of 'the' in doc 0
    print(
        f"positions of 'fox' in doc 0: {index['fox'][0]}"
    )  # => shows positions of 'fox' in doc 0

    hand_positions_the: list[int] = [
        i for i, t in enumerate(docs[0]) if t == "the"
    ]  # => an independent recount of "the"'s offsets
    hand_positions_fox: list[int] = [
        i for i, t in enumerate(docs[0]) if t == "fox"
    ]  # => an independent recount of "fox"'s offset
    assert index["the"][0] == hand_positions_the, (
        "'the' positions must match a raw offset recount"
    )  # => 'the' positions must match a raw offset recount
    assert index["fox"][0] == hand_positions_fox, (
        "'fox' positions must match a raw offset recount"
    )  # => 'fox' positions must match a raw offset recount
    print(
        f"MATCH: every term's stored positions match a raw recount of its offsets in the source document"
    )  # => shows MATCH: every term's stored positions match a raw recount of its offsets in the source document


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
