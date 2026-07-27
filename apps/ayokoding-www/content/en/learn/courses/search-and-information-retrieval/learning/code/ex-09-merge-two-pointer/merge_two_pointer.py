# pyright: strict
"""Example 9: Merge Two Pointer (co-04)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import random  # => stdlib PRNG -- reproducible synthetic fixtures and trials


def merge_and_two_pointer(
    a: list[int], b: list[int]
) -> list[
    int
]:  # => intersect two SORTED posting lists with a single linear two-pointer pass
    """Intersect two SORTED posting lists with a single linear two-pointer pass."""
    result: list[int] = []  # => accumulates matching doc-ids, in order
    i = j = 0  # => one cursor per list -- each only ever moves forward
    while i < len(a) and j < len(b):  # => stop the instant either list is exhausted
        if a[i] == b[j]:  # => a match -- record it and advance BOTH cursors
            result.append(a[i])  # => records this item, in order
            i += 1  # => advances i
            j += 1  # => advances j
        elif (
            a[i] < b[j]
        ):  # => a[i] can never match anything later in b -- advance i only
            i += 1  # => advances i
        else:  # => b[j] can never match anything later in a -- advance j only
            j += 1  # => advances j
    return result  # => every doc-id present in both a and b, ascending


def main() -> None:  # => defines main
    rng = random.Random(42)  # => fixed seed -- reproducible random trials
    for trial in range(200):  # => 200 random posting-list pairs
        size_a, size_b = (
            rng.randint(0, 20),
            rng.randint(0, 20),
        )  # => varying sizes, including empty
        a: list[int] = sorted(
            {rng.randint(0, 30) for _ in range(size_a)}
        )  # => a valid sorted posting list
        b: list[int] = sorted(
            {rng.randint(0, 30) for _ in range(size_b)}
        )  # => another valid sorted posting list
        got: list[int] = merge_and_two_pointer(
            a, b
        )  # => the two-pointer algorithm's own answer
        expected: list[int] = sorted(
            set(a) & set(b)
        )  # => the reference answer, via Python's set '&'
        assert got == expected, (
            f"trial {trial}: {a} & {b} -> got {got}, expected {expected}"
        )  # => trial {trial}: {a} & {b} -> got {got}, expected {expected}

    sample_a: list[int] = [
        1,
        3,
        5,
        7,
        9,
        11,
    ]  # => a small, readable example for the printed output
    sample_b: list[int] = [2, 3, 4, 7, 8, 11]  # => sample b = [2, 3, 4, 7, 8, 11]
    print(f"a={sample_a}")  # => shows a=
    print(f"b={sample_b}")  # => shows b=
    print(
        f"merge_and_two_pointer(a, b) = {merge_and_two_pointer(sample_a, sample_b)}"
    )  # => shows merge_and_two_pointer(a, b) =
    print(
        "MATCH: two-pointer intersection equals Python's set '&' across 200 random trials, one pass each"
    )  # => shows MATCH: two-pointer intersection equals Python's set '&' across 200 random trials, one pass each


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
