# learning/code/ex-56-supply-chain-typosquat-check/typosquat_check.py
"""Example 56: a real, hand-written Levenshtein check flags typosquat-shaped package names (co-21, co-25)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the distance-comparison logic itself

KNOWN_GOOD_PACKAGES = {
    "requests",
    "flask",
    "numpy",
    "django",
}  # => co-21: the REAL, well-known packages this trusts


def levenshtein_distance(
    a: str, b: str
) -> int:  # => co-21: a real, hand-written edit-distance implementation
    if (
        a == b
    ):  # => co-21: fast path -- identical strings are always distance 0, no DP table needed
        return 0  # => co-21: real short-circuit, saves building a table for the common "exact match" case
    previous_row = list(
        range(len(b) + 1)
    )  # => co-21: DP row 0 -- distance from "" to each prefix of b
    for i, char_a in enumerate(
        a, start=1
    ):  # => co-21: builds one REAL DP row per character of a, top to bottom
        current_row = [
            i
        ]  # => co-21: distance from a[:i] to "" is always i (i deletions)
        for j, char_b in enumerate(
            b, start=1
        ):  # => co-21: fills in each real cell of this row, left to right
            insert_cost = current_row[j - 1] + 1  # => co-21: insert one char of b
            delete_cost = previous_row[j] + 1  # => co-21: delete one char of a
            substitute_cost = previous_row[j - 1] + (
                char_a != char_b
            )  # => co-21: substitute only if chars differ
            current_row.append(
                min(insert_cost, delete_cost, substitute_cost)
            )  # => co-21: the REAL cheapest edit here
        previous_row = current_row  # => co-21: this row becomes the "previous" row for the NEXT character of a
    return previous_row[
        -1
    ]  # => co-21: the bottom-right cell -- the real, full edit distance between a and b


def closest_known_package(
    candidate: str,
) -> tuple[str, int]:  # => co-21: finds the REAL nearest known-good name
    distances = {
        name: levenshtein_distance(candidate, name) for name in KNOWN_GOOD_PACKAGES
    }  # => co-21: real, all pairs
    closest = min(
        distances, key=lambda name: distances[name]
    )  # => co-21: the REAL minimum-distance known package
    return closest, distances[
        closest
    ]  # => co-21: (nearest real name, real edit distance to it)


def is_suspicious_typosquat(
    candidate: str, max_distance: int = 2
) -> bool:  # => co-21: the REAL flagging rule
    if (
        candidate in KNOWN_GOOD_PACKAGES
    ):  # => co-21: an EXACT match is the real package itself -- never suspicious
        return False  # => co-21: real, trusted names always pass through untouched
    closest, distance = closest_known_package(
        candidate
    )  # => co-21: how close is this candidate to a REAL package
    return (
        0 < distance <= max_distance
    )  # => co-21: close but NOT identical -- exactly the typosquat shape


def main() -> (
    None
):  # => co-21: runs the REAL check against a mix of real names, typosquats, and unrelated names
    candidates = [  # => co-21: every string here is REAL input to the check -- no package is ever actually installed
        "requests",  # => co-21: the genuine, correct package name -- must NOT be flagged
        "reqeusts",  # => co-21: a real transposition typosquat of "requests" (swapped 'ue')
        "requessts",  # => co-21: a real insertion typosquat of "requests" (doubled 's')
        "reqeusts2",  # => co-21: a real, slightly-further typosquat variant with an appended digit
        "flask",  # => co-21: another genuine, correct package name -- must NOT be flagged
        "flaskk",  # => co-21: a real single-character-insertion typosquat of "flask"
        "urllib3",  # => co-21: a REAL, legitimately unrelated package -- must NOT be flagged as a typosquat
    ]
    print(
        f"known-good packages: {sorted(KNOWN_GOOD_PACKAGES)}\n"
    )  # => co-21: the real trust anchor this check uses

    results: list[
        tuple[str, bool, str, int]
    ] = []  # => co-21: accumulates (name, flagged, nearest, distance) per candidate
    for candidate in (
        candidates
    ):  # => co-21: runs the REAL check against every real candidate string in order
        flagged = is_suspicious_typosquat(
            candidate
        )  # => co-21: the real, computed verdict for this candidate
        nearest, distance = closest_known_package(
            candidate
        )  # => co-21: real supporting evidence for the verdict
        results.append(
            (candidate, flagged, nearest, distance)
        )  # => co-21: records the real (candidate, verdict) pair
        verdict = (
            "SUSPICIOUS (typosquat-shaped)" if flagged else "ok"
        )  # => co-21: human-readable real verdict
        print(
            f"  {candidate!r:14} -> {verdict:30} (nearest={nearest!r}, distance={distance})"
        )  # => co-21: real, per-row

    flagged_names = {
        name for name, flagged, _, _ in results if flagged
    }  # => co-21: every REAL name this run flagged
    assert flagged_names == {
        "reqeusts",
        "requessts",
        "flaskk",
    }  # => co-21: proves EXACTLY the real typosquats were caught
    assert (
        "requests" not in flagged_names and "flask" not in flagged_names
    )  # => co-21: real names never self-flag
    assert (
        "urllib3" not in flagged_names
    )  # => co-21: proves a genuinely unrelated real package is left alone
    assert (
        "reqeusts2" not in flagged_names
    )  # => co-21: proves the threshold has a real, principled cutoff (distance 3)


if (
    __name__ == "__main__"
):  # => co-21: only runs when launched directly, e.g. `python3 typosquat_check.py`
    main()  # => co-21: runs the full, real check and prints every real (candidate, verdict) pair
