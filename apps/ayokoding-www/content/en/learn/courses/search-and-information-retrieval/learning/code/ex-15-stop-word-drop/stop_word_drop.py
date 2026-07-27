# pyright: strict
"""Example 15: Stop-Word Drop (co-08)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

STOP_WORDS: frozenset[str] = frozenset(
    {"the", "a", "an", "of", "in", "on", "and", "or", "to", "is", "are", "for"}
)  # => STOP WORDS = frozenset({"the", "a", "an", "of", "in", "on", ...
# => co-08: a small, deliberately narrow stop-word list -- high frequency, low signal


def remove_stop_words(
    tokens: list[str],
) -> list[
    str
]:  # => drop every token that is in the stop-word list, preserving relative order
    """Drop every token that is in the stop-word list, preserving relative order."""
    return [
        t for t in tokens if t not in STOP_WORDS
    ]  # => co-08: filters out low-signal terms


def main() -> None:  # => defines main
    text: str = "the quick brown fox jumps over the lazy dog and the cat"  # => the sample document
    tokens: list[str] = [
        str(t) for t in text.split()
    ]  # => co-06: whitespace tokenization, as in Example 1 (str(t) widens pyright's LiteralString inference to plain str)
    filtered: list[str] = remove_stop_words(
        tokens
    )  # => co-08: the same tokens, stop words dropped
    print(f"before ({len(tokens)} tokens): {tokens}")  # => shows before (
    print(f"after  ({len(filtered)} tokens): {filtered}")  # => shows after  (

    assert "the" not in filtered, (
        "'the' must be fully removed by stop-word filtering"
    )  # => 'the' must be fully removed by stop-word filtering
    assert "and" not in filtered, (
        "'and' must be fully removed by stop-word filtering"
    )  # => 'and' must be fully removed by stop-word filtering
    assert len(filtered) < len(tokens), (
        "the total token count must strictly fall after removal"
    )  # => the total token count must strictly fall after removal
    print(
        f"MATCH: 'the' is absent and the token count dropped from {len(tokens)} to {len(filtered)}"
    )  # => shows MATCH: 'the' is absent and the token count dropped from


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
