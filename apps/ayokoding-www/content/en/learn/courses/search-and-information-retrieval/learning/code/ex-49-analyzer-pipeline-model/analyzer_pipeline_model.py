# pyright: strict
"""Example 49: Analyzer Pipeline Model (co-25)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => from dataclasses: dataclass, field
from typing import Callable  # => from typing: Callable


@dataclass  # => part of this step's computation, continued from the line above
class Analyzer:  # => part of this step's computation, continued from the line above
    """Char filters -> ONE tokenizer -> token filters, in that fixed order (Elastic's own model)."""

    char_filters: list[Callable[[str], str]] = field(
        default_factory=lambda: []
    )  # => co-25: text -> text, applied in order
    tokenizer: Callable[[str], list[str]] = (
        str.split
    )  # => co-25: text -> tokens, exactly ONE, never zero or many
    token_filters: list[Callable[[list[str]], list[str]]] = field(
        default_factory=lambda: []
    )  # => co-25: tokens -> tokens, in order

    def analyze(self, text: str) -> list[str]:  # => defines analyze
        for (
            char_filter
        ) in self.char_filters:  # => co-25: stage 1 -- runs BEFORE tokenization
            text = char_filter(text)  # => text = char_filter(text)
        tokens: list[str] = self.tokenizer(
            text
        )  # => co-25: stage 2 -- exactly one tokenizer call
        for token_filter in (
            self.token_filters
        ):  # => co-25: stage 3 -- runs AFTER tokenization, in order
            tokens = token_filter(tokens)  # => tokens = token_filter(tokens)
        return tokens  # => returns tokens


def strip_html(
    text: str,
) -> str:  # => a toy char filter: removes anything between angle brackets
    """A toy char filter: removes anything between angle brackets."""
    result: list[str] = []  # => starts empty, populated by the loop below
    in_tag: bool = False  # => in tag = False
    for ch in text:  # => iterates one item at a time
        if ch == "<":  # => true when ch == "<"
            in_tag = True  # => in tag = True
        elif ch == ">":  # => otherwise, true when ch == ">"
            in_tag = False  # => in tag = False
        elif not in_tag:  # => otherwise, true when not in_tag
            result.append(ch)  # => records this item, in order
    return "".join(result)  # => returns "".join(result)


def lowercase_filter(tokens: list[str]) -> list[str]:  # => defines lowercase filter
    return [t.lower() for t in tokens]  # => returns [t.lower() for t in tokens]


def main() -> None:  # => defines main
    analyzer = Analyzer(  # => co-25: assembles the 3-stage pipeline
        char_filters=[strip_html],  # => char filters = [strip_html],
        tokenizer=str.split,  # => tokenizer = str.split,
        token_filters=[lowercase_filter],  # => token filters = [lowercase_filter],
    )  # => opens/closes this multi-line literal
    text: str = "<b>Search</b> Engines are Fast"  # => HTML markup + mixed case
    result: list[str] = analyzer.analyze(
        text
    )  # => co-25: char-filter -> tokenize -> token-filter, in order
    print(f"input:  {text!r}")  # => shows input
    print(f"output: {result}")  # => shows output

    expected: list[str] = [
        "search",
        "engines",
        "are",
        "fast",
    ]  # => hand-traced: strip_html then split then lowercase
    assert result == expected, (
        f"expected {expected}, got {result}"
    )  # => expected {expected}, got {result}
    print(
        f"MATCH: the 3-stage analyzer's output equals the hand-traced fixture {expected}"
    )  # => shows MATCH: the 3-stage analyzer's output equals the hand-traced fixture


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
