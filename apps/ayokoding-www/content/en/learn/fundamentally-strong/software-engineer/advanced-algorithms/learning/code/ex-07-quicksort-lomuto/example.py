"""Example 7: Quicksort with Lomuto Partitioning."""

# Lomuto partitioning (co-08) picks the LAST element as pivot, then walks the
# range keeping a boundary "i" such that everything at or before i is <= pivot.
# Unlike merge sort, quicksort partitions and recurses IN PLACE -- no new list.
import random  # => used only to build a randomized test input


def quicksort(items: list[int], lo: int = 0, hi: int | None = None) -> None:
    if hi is None:  # => the top-level call omits hi -- default to the last index
        hi = len(items) - 1  # => sorts the WHOLE list on the first call
    if lo < hi:  # => base case: a 0- or 1-element range is already sorted
        p = lomuto_partition(items, lo, hi)  # => places the pivot at its final index
        quicksort(items, lo, p - 1)  # => recursively sorts everything left of pivot
        quicksort(items, p + 1, hi)  # => recursively sorts everything right of pivot


def lomuto_partition(items: list[int], lo: int, hi: int) -> int:  # => returns pivot idx
    pivot = items[hi]  # => Lomuto's defining choice: the LAST element is the pivot
    i = lo - 1  # => boundary of the "<=pivot" region -- starts just before lo
    for j in range(lo, hi):  # => scans every element except the pivot itself
        if items[j] <= pivot:  # => this element belongs in the "<=pivot" region
            i += 1  # => grows the "<=pivot" region by one slot
            items[i], items[j] = items[j], items[i]  # => swaps it into that region
    items[i + 1], items[hi] = items[hi], items[i + 1]  # => places pivot right after
    return i + 1  # => the pivot's final, correct sorted-position index


random.seed(11)  # => fixed seed -> reproducible "random" input
data: list[int] = random.sample(range(1, 500), 30)  # => 30 distinct random ints
expected = sorted(data)  # => Python's own sort, as ground truth
quicksort(data)  # => sorts `data` IN PLACE -- no return value to capture
print(data == expected)  # => Output: True
print(data[:5])  # => Output: the 5 smallest values, ascending

assert data == expected  # => confirms in-place quicksort matches sorted()
sorted_input: list[int] = [1, 2, 3, 4, 5]  # => an already-sorted 5-element list
quicksort(sorted_input)  # => sorting an already-sorted list is a valid edge case
assert sorted_input == [1, 2, 3, 4, 5]  # => confirms it stays correctly sorted
print("ex-07 OK")  # => Output: ex-07 OK
