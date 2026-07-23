"""Example 75: Kth Smallest via Quickselect."""

import random  # => used to pick a random pivot, avoiding worst-case behavior


# Partitions like quicksort, but recurses into only ONE side -- O(n) average,
# versus sorting the whole list first at O(n log n) (co-16).
def quickselect(
    items: list[int], k: int
) -> int:  # => a partition-driven recursive function
    if len(items) == 1:  # => BASE CASE -- one element left; it must be the answer
        return items[0]  # => the only candidate remaining
    pivot = random.choice(
        items
    )  # => a random pivot avoids worst-case O(n^2) on sorted input
    less = [x for x in items if x < pivot]  # => strictly smaller than pivot
    equal = [x for x in items if x == pivot]  # => every occurrence of the pivot itself
    greater = [x for x in items if x > pivot]  # => strictly larger than pivot
    if k < len(less):  # => the target rank lives entirely within the "less" partition
        return quickselect(less, k)  # => RECURSE into just ONE side -- discard the rest
    if k < len(less) + len(
        equal
    ):  # => the target rank falls within the pivot's own value(s)
        return pivot  # => found it -- no further recursion needed
    return quickselect(
        greater, k - len(less) - len(equal)
    )  # => recurse right, rank shifted


values = [7, 2, 9, 4, 1, 8, 3]  # => 7 unsorted values, 0-indexed ranks 0..6
third_smallest = quickselect(
    values, 2
)  # => rank 2 (0-indexed) == the 3rd smallest overall
print(third_smallest)  # => Output: 3

assert (
    third_smallest == sorted(values)[2]
)  # => cross-checks against a plain sort at the same rank
print("ex-75 OK")  # => Output: ex-75 OK
