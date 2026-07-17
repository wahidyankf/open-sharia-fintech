"""Example 13: Stable sorted() vs an Unstable Selection Sort on (key, seq) Pairs."""

# A stable sort (co-11) preserves the INPUT order of records that share a key.
# sorted() is documented-stable; a classic swap-based selection sort is NOT --
# a single swap can leapfrog one equal-key element past another.


def stable_sort_by_key(
    pairs: list[tuple[int, str]],
) -> list[tuple[int, str]]:  # => Timsort, guaranteed stable
    return sorted(pairs, key=lambda p: p[0])  # => sorts by key only, ties keep order


def selection_sort_by_key(
    pairs: list[tuple[int, str]],
) -> list[tuple[int, str]]:  # => the classic textbook selection sort -- NOT stable
    items = list(pairs)  # => a working copy -- the caller's list is never mutated
    n = len(items)  # => n = number of (key, seq) records
    for i in range(n):  # => grows the sorted prefix by one record each pass
        min_idx = i  # => assumes position i holds the smallest remaining key so far
        for j in range(i + 1, n):  # => scans the unsorted remainder for a smaller key
            if items[j][0] < items[min_idx][0]:  # => strictly smaller key found
                min_idx = j  # => tracks the new candidate minimum's index
        items[i], items[min_idx] = (
            items[min_idx],
            items[i],
        )  # => THE SWAP that can break stability -- it can jump an equal-key element
    return items  # => sorted by key, but relative order of ties is NOT guaranteed


data: list[tuple[int, str]] = [
    (1, "a"),
    (1, "b"),
    (0, "c"),
]  # => two records share key=1: "a" then "b", in that input order
stable_result = stable_sort_by_key(data)  # => sorted() -- documented stable
unstable_result = selection_sort_by_key(data)  # => selection sort -- not stable
print(stable_result)  # => Output: [(0, 'c'), (1, 'a'), (1, 'b')]
print(unstable_result)  # => Output: [(0, 'c'), (1, 'b'), (1, 'a')]

assert stable_result == [
    (0, "c"),
    (1, "a"),
    (1, "b"),
]  # => "a" stays before "b" -- input order preserved for the tied key
assert unstable_result == [
    (0, "c"),
    (1, "b"),
    (1, "a"),
]  # => "b" now precedes "a" -- the swap silently reordered the tie
assert stable_result != unstable_result  # => same keys sorted, different tie order
print("ex-13 OK")  # => Output: ex-13 OK
