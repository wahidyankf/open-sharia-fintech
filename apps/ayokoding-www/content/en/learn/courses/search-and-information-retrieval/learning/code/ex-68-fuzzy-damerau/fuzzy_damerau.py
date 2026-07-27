# pyright: strict
"""Example 68: Fuzzy: Damerau (co-32)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def levenshtein(a: str, b: str) -> int:  # => defines levenshtein
    rows, cols = (
        len(a) + 1,
        len(b) + 1,
    )  # => part of this step's computation, continued from the line above
    dp: list[list[int]] = [
        [0] * cols for _ in range(rows)
    ]  # => dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):  # => iterates one item at a time
        dp[i][0] = i  # => dp = i
    for j in range(cols):  # => iterates one item at a time
        dp[0][j] = j  # => dp = j
    for i in range(1, rows):  # => iterates one item at a time
        for j in range(1, cols):  # => iterates one item at a time
            if a[i - 1] == b[j - 1]:  # => true when a[i - 1] == b[j - 1]
                dp[i][j] = dp[i - 1][j - 1]  # => dp = dp[i - 1][j - 1]
            else:  # => the fallback branch, when no prior condition matched
                dp[i][j] = 1 + min(
                    dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]
                )  # => dp = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j...
    return dp[rows - 1][cols - 1]  # => returns dp[rows - 1][cols - 1]


def damerau_levenshtein(
    a: str, b: str
) -> int:  # => levenshtein PLUS a transposition operation: swapping two ADJACENT characters costs 1, not 2
    """Levenshtein PLUS a transposition operation: swapping two ADJACENT characters costs 1, not 2."""
    rows, cols = (
        len(a) + 1,
        len(b) + 1,
    )  # => part of this step's computation, continued from the line above
    dp: list[list[int]] = [
        [0] * cols for _ in range(rows)
    ]  # => dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):  # => iterates one item at a time
        dp[i][0] = i  # => dp = i
    for j in range(cols):  # => iterates one item at a time
        dp[0][j] = j  # => dp = j

    for i in range(1, rows):  # => iterates one item at a time
        for j in range(1, cols):  # => iterates one item at a time
            cost: int = (
                0 if a[i - 1] == b[j - 1] else 1
            )  # => 0 for a match, 1 for a substitution
            dp[i][j] = min(  # => dp = min(
                dp[i - 1][j] + 1,  # => delete
                dp[i][j - 1] + 1,  # => insert
                dp[i - 1][j - 1] + cost,  # => match or substitute
            )  # => opens/closes this multi-line literal
            if (  # => co-32: the EXTRA Damerau case -- an adjacent transposition
                i
                > 1  # => part of this step's computation, continued from the line above
                and j
                > 1  # => part of this step's computation, continued from the line above
                and a[i - 1]
                == b[
                    j - 2
                ]  # => part of this step's computation, continued from the line above
                and a[i - 2]
                == b[
                    j - 1
                ]  # => part of this step's computation, continued from the line above
            ):  # => part of this step's computation, continued from the line above
                dp[i][j] = min(
                    dp[i][j], dp[i - 2][j - 2] + 1
                )  # => co-32: ONE swap, not two edits
    return dp[rows - 1][cols - 1]  # => returns dp[rows - 1][cols - 1]


def main() -> None:  # => defines main
    plain_distance: int = levenshtein(
        "teh", "the"
    )  # => co-32: plain Levenshtein sees 'teh'->'the' as TWO edits
    damerau_distance: int = damerau_levenshtein(
        "teh", "the"
    )  # => co-32: Damerau sees the SAME pair as ONE swap
    print(
        f"levenshtein('teh', 'the') = {plain_distance}"
    )  # => shows levenshtein('teh', 'the') =
    print(
        f"damerau_levenshtein('teh', 'the') = {damerau_distance}"
    )  # => shows damerau_levenshtein('teh', 'the') =

    assert plain_distance == 2, (
        "plain Levenshtein must score 'teh'->'the' as distance 2 (substitute+substitute, or del+ins)"
    )  # => plain Levenshtein must score 'teh'->'the' as distance 2 (substitute+substitute, or del+ins)
    assert damerau_distance == 1, (
        "Damerau-Levenshtein must score the SAME pair as distance 1 (one adjacent swap)"
    )  # => Damerau-Levenshtein must score the SAME pair as distance 1 (one adjacent swap)
    print(
        f"MATCH: the identical typo scores {plain_distance} under plain Levenshtein but {damerau_distance} under Damerau -- transpositions are cheap typos"
    )  # => shows MATCH: the identical typo scores


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
