# pyright: strict
"""Example 69: Spelling Correct (co-32)."""

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


def suggest_correction(
    misspelled: str, dictionary: list[str]
) -> str:  # => return the dictionary term with the SMALLEST edit distance to misspelled
    """Return the dictionary term with the SMALLEST edit distance to misspelled."""
    best_term: str = dictionary[
        0
    ]  # => co-32: starts with the first candidate as the running best
    best_distance: int = levenshtein(
        misspelled, best_term
    )  # => best distance = levenshtein(misspelled, best_term)
    for term in dictionary[1:]:  # => checks EVERY remaining candidate
        distance: int = levenshtein(
            misspelled, term
        )  # => distance = levenshtein(misspelled, term)
        if (
            distance < best_distance
        ):  # => co-32: strictly BETTER -- replaces the running best
            best_term, best_distance = (
                term,
                distance,
            )  # => part of this step's computation, continued from the line above
    return best_term  # => returns best_term


def main() -> None:  # => defines main
    dictionary: list[str] = [
        "search",
        "engine",
        "ranking",
        "index",
        "query",
    ]  # => the known-good vocabulary
    misspelled: str = "serch"  # => a typo of "search" -- missing the 'a'

    suggestion: str = suggest_correction(
        misspelled, dictionary
    )  # => co-32: the closest dictionary term
    print(
        f"misspelled: {misspelled!r}  suggestion: {suggestion!r}"
    )  # => shows misspelled

    hand_distances: dict[str, int] = {
        term: levenshtein(misspelled, term) for term in dictionary
    }  # => an INDEPENDENT recount of every distance
    for term, dist in sorted(
        hand_distances.items(), key=lambda kv: kv[1]
    ):  # => iterates one item at a time
        print(f"  distance to {term!r}: {dist}")  # => shows distance to

    hand_best: str = min(
        hand_distances, key=lambda t: hand_distances[t]
    )  # => the minimum, computed a DIFFERENT way
    assert suggestion == hand_best, (
        "suggest_correction's result must equal the independently-recomputed minimum"
    )  # => suggest_correction's result must equal the independently-recomputed minimum
    assert suggestion == "search", (
        "'serch' must correct to 'search', its true nearest dictionary neighbor"
    )  # => 'serch' must correct to 'search', its true nearest dictionary neighbor
    print(
        f"MATCH: suggest_correction's {suggestion!r} equals the independently verified minimum-distance term"
    )  # => shows MATCH: suggest_correction's


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
