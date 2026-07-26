# pyright: strict
"""Example 67: Fuzzy: Levenshtein (co-32)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def levenshtein(
    a: str, b: str
) -> int:  # => classic O(len(a) * len(b)) edit-distance dynamic-programming table
    """Classic O(len(a) * len(b)) edit-distance dynamic-programming table."""
    rows, cols = (
        len(a) + 1,
        len(b) + 1,
    )  # => co-32: +1 for the "empty prefix" row/column
    dp: list[list[int]] = [
        [0] * cols for _ in range(rows)
    ]  # => the DP table, all zeros initially
    for i in range(rows):  # => iterates one item at a time
        dp[i][0] = i  # => co-32: transforming a[:i] into "" costs i deletions
    for j in range(cols):  # => iterates one item at a time
        dp[0][j] = j  # => co-32: transforming "" into b[:j] costs j insertions

    for i in range(1, rows):  # => fills the table row by row
        for j in range(1, cols):  # => iterates one item at a time
            if a[i - 1] == b[j - 1]:  # => co-32: matching characters cost NOTHING extra
                dp[i][j] = dp[i - 1][j - 1]  # => dp = dp[i - 1][j - 1]
            else:  # => the fallback branch, when no prior condition matched
                dp[i][j] = (
                    1
                    + min(  # => co-32: 1 + the cheapest of delete, insert, substitute
                        dp[i - 1][j],  # => delete a[i-1]
                        dp[i][j - 1],  # => insert b[j-1]
                        dp[i - 1][j - 1],  # => substitute a[i-1] for b[j-1]
                    )
                )  # => opens/closes this multi-line literal
    return dp[rows - 1][
        cols - 1
    ]  # => co-32: the bottom-right cell holds the FULL-string edit distance


def main() -> None:  # => defines main
    distance: int = levenshtein(
        "colour", "color"
    )  # => co-32: British vs American spelling
    print(
        f"levenshtein('colour', 'color') = {distance}"
    )  # => shows levenshtein('colour', 'color') =

    identical: int = levenshtein(
        "search", "search"
    )  # => the SAME string -- must be distance 0
    very_different: int = levenshtein(
        "cat", "dog"
    )  # => no shared characters at matching positions
    print(
        f"levenshtein('search', 'search') = {identical}"
    )  # => shows levenshtein('search', 'search') =
    print(
        f"levenshtein('cat', 'dog') = {very_different}"
    )  # => shows levenshtein('cat', 'dog') =

    assert distance == 1, (
        "'colour' -> 'color' is exactly ONE deletion (the 'u') -- distance must be 1"
    )  # => 'colour' -> 'color' is exactly ONE deletion (the 'u') -- distance must be 1
    assert identical == 0, (
        "identical strings must have distance 0"
    )  # => identical strings must have distance 0
    assert very_different == 3, (
        "'cat' -> 'dog' shares no aligned characters -- distance must be 3 (full substitution)"
    )  # => 'cat' -> 'dog' shares no aligned characters -- distance must be 3 (full substitution)
    print(
        f"MATCH: colour/color={distance}, identical={identical}, cat/dog={very_different} -- all match hand-verified edit distances"
    )  # => shows MATCH: colour/color=


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
