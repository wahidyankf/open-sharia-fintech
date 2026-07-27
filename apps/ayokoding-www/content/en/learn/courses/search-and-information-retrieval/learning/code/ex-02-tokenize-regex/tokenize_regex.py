# pyright: strict
"""Example 2: Tokenize Regex (co-06)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import re  # => stdlib regex -- the \w+ tokenizer pattern

TOKEN_PATTERN: re.Pattern[str] = re.compile(
    r"\w+"
)  # => matches runs of word chars, dropping punctuation


def tokenize_regex(
    text: str,
) -> list[str]:  # => tokenize text with a \\w+ regex, discarding all punctuation
    """Tokenize text with a \\w+ regex, discarding all punctuation."""
    return TOKEN_PATTERN.findall(text)  # => every maximal run of [A-Za-z0-9_], in order


def main() -> None:  # => defines main
    with_period: str = (
        "this is the end."  # => a sentence ending in a period right after "end"
    )
    without_period: str = "this is the end"  # => the SAME sentence, no trailing period
    tokens_with: list[str] = tokenize_regex(
        with_period
    )  # => co-06: regex tokenization strips "."
    tokens_without: list[str] = tokenize_regex(
        without_period
    )  # => no punctuation to strip here
    print(f"tokens (with period): {tokens_with}")  # => shows tokens (with period)
    print(
        f"tokens (without period): {tokens_without}"
    )  # => shows tokens (without period)

    assert tokens_with[-1] == "end", (
        "the regex tokenizer must drop the trailing period"
    )  # => the regex tokenizer must drop the trailing period
    assert tokens_with == tokens_without, (
        "'end.' and 'end' must tokenize to the identical token list"
    )  # => 'end.' and 'end' must tokenize to the identical token list
    print(
        "MATCH: 'end.' and 'end' tokenize to the identical list -- punctuation carries no weight to \\w+"
    )  # => shows MATCH: 'end.' and 'end' tokenize to the identical list -- punctuation carries no weight to \\w+


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
