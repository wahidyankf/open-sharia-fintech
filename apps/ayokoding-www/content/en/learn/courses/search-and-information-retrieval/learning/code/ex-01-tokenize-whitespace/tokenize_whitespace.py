# pyright: strict
"""Example 1: Tokenize Whitespace (co-06)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def tokenize_whitespace(
    text: str,
) -> list[str]:  # => split text into tokens on any run of whitespace
    """Split text into tokens on any run of whitespace."""
    return (
        text.split()
    )  # => str.split() with no args splits on runs of whitespace, drops empties


def main() -> None:  # => defines main
    document: str = (
        "the quick brown fox jumps over the lazy dog"  # => 9 space-separated words
    )
    tokens: list[str] = tokenize_whitespace(
        document
    )  # => co-06: the first stage of every index pipeline
    print(f"document: {document!r}")  # => shows document
    print(f"tokens: {tokens}")  # => shows tokens
    print(f"token count: {len(tokens)}")  # => shows token count

    expected_count: int = len(
        document.split(" ")
    )  # => an independent count: split on literal " "
    assert len(tokens) == expected_count, (
        "token count must equal the space-separated word count"
    )  # => token count must equal the space-separated word count
    print(
        f"MATCH: token count ({len(tokens)}) equals the space-separated word count ({expected_count})"
    )  # => shows MATCH: token count (


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
