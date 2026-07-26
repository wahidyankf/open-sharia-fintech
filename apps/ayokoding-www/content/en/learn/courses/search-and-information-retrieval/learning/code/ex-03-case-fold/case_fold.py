# pyright: strict
"""Example 3: Case Fold (co-07)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def case_fold(
    tokens: list[str],
) -> list[str]:  # => lowercase every token so case variants conflate to one index term
    """Lowercase every token so case variants conflate to one index term."""
    return [
        t.lower() for t in tokens
    ]  # => str.lower() -- the standard ASCII/Unicode case fold


def main() -> None:  # => defines main
    tokens: list[str] = [
        "The",
        "the",
        "THE",
        "ThE",
    ]  # => four case variants of the same word
    folded: list[str] = case_fold(
        tokens
    )  # => co-07: every variant becomes the SAME index term
    print(f"before: {tokens}")  # => shows before
    print(f"after:  {folded}")  # => shows after

    unique_before: set[str] = set(tokens)  # => 4 distinct strings before folding
    unique_after: set[str] = set(folded)  # => how many distinct strings survive folding
    print(
        f"unique before: {len(unique_before)} | unique after: {len(unique_after)}"
    )  # => shows unique before

    assert len(unique_after) == 1, (
        "all four case variants must collapse to exactly one term"
    )  # => all four case variants must collapse to exactly one term
    assert folded[0] == folded[1] == "the", (
        "'The' and 'the' must both fold to 'the'"
    )  # => 'The' and 'the' must both fold to 'the'
    print(
        "MATCH: 'The' and 'the' (and every other case variant) collapse to the single term 'the'"
    )  # => shows MATCH: 'The' and 'the' (and every other case variant) collapse to the single term 'the'


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
