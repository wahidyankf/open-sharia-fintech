"""Kata 5 (after): fix -- a None sentinel builds a FRESH dict on every call, reduce folds over it."""

from functools import reduce


def histogram(words: list[str], counts: dict[str, int] | None = None) -> dict[str, int]:
    start: dict[str, int] = (
        counts if counts is not None else {}
    )  # => fresh dict every call
    return reduce(
        lambda acc, w: {**acc, w: acc.get(w, 0) + 1}, words, start
    )  # => builds NEW dicts


first_doc = histogram(["a", "b", "a"])
print(first_doc)
second_doc = histogram(
    ["c"]
)  # a fresh, empty accumulator every time the default is used
print(second_doc)  # correctly isolated from the first, unrelated call
