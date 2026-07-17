"""Example 27: Randomized-Pivot Quicksort -- Sorted Input No Longer Degrades."""

# Example 8's naive quicksort always picks the FIRST element, so sorted input
# triggers its O(n^2) worst case. Picking a RANDOM pivot each time (co-08)
# makes that worst case astronomically unlikely -- expected O(n log n) even
# on already-sorted input, because the bad case no longer depends on the DATA.
import random

comparisons = 0  # => a global counter, reset before each measurement below


def randomized_quicksort(items: list[int], lo: int = 0, hi: int | None = None) -> None:
    global comparisons  # => this function mutates the module-level counter
    if hi is None:  # => top-level call defaults hi to the last index
        hi = len(items) - 1  # => sorts the WHOLE list on the first call
    if lo < hi:  # => base case: 0 or 1 elements need no partitioning
        p = random_pivot_partition(items, lo, hi)  # => the only change from Example 8
        randomized_quicksort(items, lo, p - 1)  # => recurses on the left partition
        randomized_quicksort(items, p + 1, hi)  # => recurses on the right partition


def random_pivot_partition(items: list[int], lo: int, hi: int) -> int:
    global comparisons  # => mutates the shared counter
    rand_index = random.randint(lo, hi)  # => picks a UNIFORMLY random index as pivot
    items[rand_index], items[lo] = (  # => opens the swap-to-front tuple assignment
        items[lo],  # => the old first element moves to the random index's old slot
        items[rand_index],  # => the randomly chosen value moves to the front
    )  # => swaps it to the front so the rest of the logic is unchanged
    pivot = items[lo]  # => now behaves exactly like Example 8's first-pivot partition
    i = lo  # => boundary of the "<pivot" region
    for j in range(lo + 1, hi + 1):  # => scans every element after the pivot
        comparisons += 1  # => counts this one comparison against the pivot
        if items[j] < pivot:  # => belongs strictly before the pivot
            i += 1  # => grows the "<pivot" region
            items[i], items[j] = items[j], items[i]  # => swaps it in
    items[lo], items[i] = items[i], items[lo]  # => places the pivot at its final spot
    return i  # => pivot's final index


random.seed(99)  # => fixed seed -- makes the "random" pivot choices reproducible
n = 500  # => how many elements to sort
already_sorted: list[int] = list(  # => opens the pre-sorted input construction
    range(n)  # => builds 0, 1, 2, ..., n-1 in ascending order
)  # => Example 8's worst case: pre-sorted input
naive_worst_case = n * (n - 1) // 2  # => what Example 8 would score on this same input
comparisons = 0  # => resets the shared counter before measuring
randomized_quicksort(already_sorted)  # => sorts the SAME kind of worst-case input
print(comparisons < naive_worst_case)  # => Output: True
print(already_sorted == list(range(n)))  # => Output: True -- still sorts correctly

assert (  # => opens the check -- wraps the long boolean across two lines
    comparisons < naive_worst_case  # => True only if randomization avoided the blow-up
)  # => confirms randomization avoids the O(n^2) sorted-input trap
assert already_sorted == list(range(n))  # => confirms correctness is unaffected
print("ex-27 OK")  # => Output: ex-27 OK
