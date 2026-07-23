"""Kata 5 (before): a mutable default argument silently shares ONE accumulator across every call."""


def histogram(
    words: list[str], counts: dict[str, int] = {}
) -> dict[str, int]:  # SMELL: mutable default
    for w in words:
        counts[w] = (
            counts.get(w, 0) + 1
        )  # BUG: mutates the SHARED default dict object in place
    return counts


first_doc = histogram(["a", "b", "a"])
print(first_doc)
second_doc = histogram(
    ["c"]
)  # an UNRELATED document -- should start from a fresh, empty count
print(
    second_doc
)  # BUG: "c" is mixed in with leftover counts from the first, unrelated call
