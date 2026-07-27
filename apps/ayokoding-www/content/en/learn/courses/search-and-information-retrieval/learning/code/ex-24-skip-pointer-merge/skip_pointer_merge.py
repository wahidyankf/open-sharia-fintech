# pyright: strict
"""Example 24: Skip-Pointer Merge (co-05)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import math  # => stdlib math -- log/sqrt for idf, cosine, and skip-pointer spacing


def build_skip_pointers(
    postings: list[int],
) -> dict[int, int]:  # => defines build skip pointers
    p: int = len(postings)  # => this fixture's own size
    if p == 0:  # => true when p == 0
        return {}  # => returns {}
    skip_distance: int = max(
        1, round(math.sqrt(p))
    )  # => skip distance = max(1, round(math.sqrt(p)))
    skips: dict[int, int] = {}  # => starts empty, populated by the loop below
    i: int = 0  # => a running counter, starting at zero
    while i + skip_distance < p:  # => loops while the condition holds
        skips[i] = i + skip_distance  # => skips = i + skip_distance
        i += skip_distance  # => part of this step's computation, continued from the line above
    return skips  # => returns skips


def merge_plain(
    a: list[int], b: list[int]
) -> tuple[
    list[int], int
]:  # => the Example 9 two-pointer merge, now also counting doc-id comparisons made
    """The Example 9 two-pointer merge, now also counting doc-id comparisons made."""
    result: list[int] = []  # => starts empty, populated by the loop below
    comparisons: int = (
        0  # => co-05: this is the cost the skip version below aims to reduce
    )
    i = j = 0  # => two cursors, both starting at the beginning
    while i < len(a) and j < len(b):  # => loops while the condition holds
        comparisons += 1  # => one comparison per loop iteration
        if a[i] == b[j]:  # => true when a[i] == b[j]
            result.append(a[i])  # => records this item, in order
            i += 1  # => advances i
            j += 1  # => advances j
        elif a[i] < b[j]:  # => otherwise, true when a[i] < b[j]
            i += 1  # => advances i
        else:  # => the fallback branch, when no prior condition matched
            j += 1  # => advances j
    return result, comparisons  # => returns result, comparisons


def merge_with_skips(
    a: list[int], skips_a: dict[int, int], b: list[int]
) -> tuple[
    list[int], int
]:  # => aND-intersect a (which HAS skip pointers) against b, using skips to bypass dead stretches
    """AND-intersect a (which HAS skip pointers) against b, using skips to bypass dead stretches."""
    result: list[int] = []  # => starts empty, populated by the loop below
    comparisons: int = 0  # => a running counter, starting at zero
    i = j = 0  # => two cursors, both starting at the beginning
    while i < len(a) and j < len(b):  # => loops while the condition holds
        comparisons += 1  # => advances comparisons
        if a[i] == b[j]:  # => true when a[i] == b[j]
            result.append(a[i])  # => records this item, in order
            i += 1  # => advances i
            j += 1  # => advances j
        elif a[i] < b[j]:  # => otherwise, true when a[i] < b[j]
            if (
                i in skips_a and skips_a[i] < len(a) and a[skips_a[i]] <= b[j]
            ):  # => co-05: can we SKIP ahead safely?
                i = skips_a[
                    i
                ]  # => jumps multiple entries in ONE step instead of one at a time
            else:  # => the fallback branch, when no prior condition matched
                i += 1  # => advances i
        else:  # => the fallback branch, when no prior condition matched
            j += 1  # => advances j
    return result, comparisons  # => returns result, comparisons


def main() -> None:  # => defines main
    a: list[int] = list(range(0, 2000, 2))  # => 1000 doc-ids: even numbers 0..1998
    skips_a: dict[int, int] = build_skip_pointers(a)  # => co-05: a's own skip structure
    b: list[int] = [
        1900,
        1902,
        1998,
    ]  # => b only overlaps with a's FAR end -- a long dead stretch to skip over

    plain_result, plain_comparisons = merge_plain(
        a, b
    )  # => the baseline, one step at a time
    skip_result, skip_comparisons = merge_with_skips(
        a, skips_a, b
    )  # => co-05: using the shortcuts
    print(
        f"plain merge:  result={plain_result}  comparisons={plain_comparisons}"
    )  # => shows plain merge:  result=
    print(
        f"skip merge:   result={skip_result}  comparisons={skip_comparisons}"
    )  # => shows skip merge:   result=

    assert skip_result == plain_result, (
        "the skip-pointer merge must return the IDENTICAL result"
    )  # => the skip-pointer merge must return the IDENTICAL result
    assert skip_comparisons < plain_comparisons, (
        "the skip-pointer merge must take FEWER comparisons on a long dead stretch"
    )  # => the skip-pointer merge must take FEWER comparisons on a long dead stretch
    print(
        f"MATCH: identical result, and skip merge used {skip_comparisons} comparisons vs plain merge's {plain_comparisons}"
    )  # => shows MATCH: identical result, and skip merge used


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
