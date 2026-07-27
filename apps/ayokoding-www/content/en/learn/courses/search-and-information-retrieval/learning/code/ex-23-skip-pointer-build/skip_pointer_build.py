# pyright: strict
"""Example 23: Skip-Pointer Build (co-05)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def build_skip_pointers(
    postings: list[int],
) -> dict[
    int, int
]:  # => return a source-index -> target-index map of sqrt(P)-spaced skip pointers
    """Return a source-index -> target-index map of sqrt(P)-spaced skip pointers."""
    p: int = len(postings)  # => P, the posting list's own length
    if p == 0:  # => true when p == 0
        return {}  # => returns {}
    skip_distance: int = max(
        1, round(math.sqrt(p))
    )  # => co-05: the classic sqrt(P) spacing
    skips: dict[
        int, int
    ] = {}  # => source index -> target index (both index INTO postings)
    i: int = 0  # => a running counter, starting at zero
    while (
        i + skip_distance < p
    ):  # => stop once a skip would land past the end of the list
        skips[i] = (
            i + skip_distance
        )  # => this entry's own shortcut, skip_distance ahead
        i += skip_distance  # => advance by the SAME spacing to place the next skip
    return skips  # => returns skips


def main() -> None:  # => defines main
    postings: list[int] = list(
        range(0, 200, 2)
    )  # => 100 evenly-spaced doc-ids: 0, 2, 4, ..., 198
    skips: dict[int, int] = build_skip_pointers(
        postings
    )  # => co-05: this list's own skip structure
    print(f"posting list length: {len(postings)}")  # => shows posting list length
    print(
        f"skip pointers (index -> index): {skips}"
    )  # => shows skip pointers (index -> index)
    print(
        f"skip spacing: ~{round(len(postings) ** 0.5)} (sqrt of {len(postings)})"
    )  # => shows skip spacing: ~

    for (
        source,
        target,
    ) in skips.items():  # => every single skip pointer, not just a sample
        assert target > source, (
            f"skip target {target} must be strictly ahead of source {source}"
        )  # => skip target {target} must be strictly ahead of source {source}
        assert target < len(postings), (
            f"skip target {target} must stay within the posting list"
        )  # => skip target {target} must stay within the posting list
    print(
        f"MATCH: all {len(skips)} skip targets are strictly ahead of their source and within bounds"
    )  # => shows MATCH: all


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
