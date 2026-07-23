"""Example 13: Stable sorted() vs an Unstable Selection Sort on (key, seq) Pairs."""

# A stable sort (co-11) preserves the INPUT order of records that share a key.
# sorted() is documented-stable; a classic swap-based selection sort is NOT --
# a single swap can leapfrog one equal-key element past another.


def stable_sort_by_key(  # => wraps the builtin sorted() to make its stability explicit
    pairs: list[tuple[int, str]],  # => each record is (sort key, tie-break label)
) -> list[tuple[int, str]]:  # => Timsort, guaranteed stable
    return sorted(pairs, key=lambda p: p[0])  # => sorts by key only, ties keep order


def selection_sort_by_key(  # => finds the min by index, then swaps it into place
    pairs: list[tuple[int, str]],  # => same record shape as the stable version
) -> list[tuple[int, str]]:  # => the classic textbook selection sort -- NOT stable
    items = list(pairs)  # => a working copy -- the caller's list is never mutated
    n = len(items)  # => n = number of (key, seq) records
    for i in range(n):  # => grows the sorted prefix by one record each pass
        min_idx = i  # => assumes position i holds the smallest remaining key so far
        for j in range(i + 1, n):  # => scans the unsorted remainder for a smaller key
            if items[j][0] < items[min_idx][0]:  # => strictly smaller key found
                min_idx = j  # => tracks the new candidate minimum's index
        items[i], items[min_idx] = (  # => tuple-swap -- a single atomic reassignment
            items[min_idx],  # => the found minimum moves into position i
            items[i],  # => whatever was at i moves to the minimum's old slot
        )  # => THE SWAP that can break stability -- it can jump an equal-key element
    return items  # => sorted by key, but relative order of ties is NOT guaranteed


data: list[tuple[int, str]] = [  # => the input records, deliberately unsorted by key
    (1, "a"),  # => key=1, tagged "a" -- appears BEFORE "b" in the input
    (1, "b"),  # => key=1, tagged "b" -- ties with "a" on key alone
    (0, "c"),  # => the only key=0 record -- always sorts first regardless of stability
]  # => two records share key=1: "a" then "b", in that input order
stable_result = stable_sort_by_key(data)  # => sorted() -- documented stable
unstable_result = selection_sort_by_key(data)  # => selection sort -- not stable
print(stable_result)  # => Output: [(0, 'c'), (1, 'a'), (1, 'b')]
print(unstable_result)  # => Output: [(0, 'c'), (1, 'b'), (1, 'a')]

assert stable_result == [  # => opens the expected order for the stable path
    (0, "c"),  # => key=0 always sorts first -- no tie to break here
    (1, "a"),  # => "a" retained its earlier input position relative to "b"
    (1, "b"),  # => "b" stayed after "a" -- stability held
]  # => "a" stays before "b" -- input order preserved for the tied key
assert unstable_result == [  # => opens the expected order for the unstable path
    (0, "c"),  # => key=0 still sorts first -- untouched by the swap
    (1, "b"),  # => "b" now comes first among the tied pair -- order flipped
    (1, "a"),  # => "a" was leapfrogged by the min-index swap
]  # => "b" now precedes "a" -- the swap silently reordered the tie
assert stable_result != unstable_result  # => same keys sorted, different tie order
print("ex-13 OK")  # => Output: ex-13 OK
