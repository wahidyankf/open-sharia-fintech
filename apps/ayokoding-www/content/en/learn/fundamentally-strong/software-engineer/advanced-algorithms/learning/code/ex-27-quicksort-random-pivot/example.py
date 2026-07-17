"""Example 27: Randomized-Pivot Quicksort -- Sorted Input No Longer Degrades."""

# Example 8's naive quicksort always picks the FIRST element, so sorted input
# triggers its O(n^2) worst case. Picking a RANDOM pivot each time (co-08)
# makes that worst case astronomically unlikely -- expected O(n log n) even
# on already-sorted input, because the bad case no longer depends on the DATA.
import random

comparisons = 0  # => a global counter, reset before each measurement below


def randomized_quicksort(items: list[int], lo: int = 0, hi: int | None = None) -> None:
    global comparisons
    if hi is None:
        hi = len(items) - 1
    if lo < hi:
        p = random_pivot_partition(items, lo, hi)  # => the only change from Example 8
        randomized_quicksort(items, lo, p - 1)
        randomized_quicksort(items, p + 1, hi)


def random_pivot_partition(items: list[int], lo: int, hi: int) -> int:
    global comparisons
    rand_index = random.randint(lo, hi)  # => picks a UNIFORMLY random index as pivot
    items[rand_index], items[lo] = (
        items[lo],
        items[rand_index],
    )  # => swaps it to the front so the rest of the logic is unchanged
    pivot = items[lo]  # => now behaves exactly like Example 8's first-pivot partition
    i = lo
    for j in range(lo + 1, hi + 1):
        comparisons += 1
        if items[j] < pivot:
            i += 1
            items[i], items[j] = items[j], items[i]
    items[lo], items[i] = items[i], items[lo]
    return i


random.seed(99)  # => fixed seed -- makes the "random" pivot choices reproducible
n = 500  # => how many elements to sort
already_sorted: list[int] = list(
    range(n)
)  # => Example 8's worst case: pre-sorted input
naive_worst_case = n * (n - 1) // 2  # => what Example 8 would score on this same input
comparisons = 0  # => resets the shared counter before measuring
randomized_quicksort(already_sorted)  # => sorts the SAME kind of worst-case input
print(comparisons < naive_worst_case)  # => Output: True
print(already_sorted == list(range(n)))  # => Output: True -- still sorts correctly

assert (
    comparisons < naive_worst_case
)  # => confirms randomization avoids the O(n^2) sorted-input trap
assert already_sorted == list(range(n))  # => confirms correctness is unaffected
print("ex-27 OK")  # => Output: ex-27 OK
