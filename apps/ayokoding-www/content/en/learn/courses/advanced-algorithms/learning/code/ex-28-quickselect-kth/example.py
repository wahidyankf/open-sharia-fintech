"""Example 28: Quickselect -- the k-th Smallest Element in Expected O(n)."""

# Quickselect (co-08) reuses quicksort's partition step, but RECURSES INTO
# ONLY ONE SIDE -- whichever side contains the k-th position -- instead of
# both, giving expected O(n) instead of a full O(n log n) sort.
import random


def quickselect(  # => recurses into only the side containing rank k, not both sides
    items: list[int],  # => the array to search within (never mutated by the caller)
    k: int,  # => k is the 0-indexed target rank to find
) -> int:  # => returns the k-th smallest (0-indexed)
    working = list(items)  # => a copy -- the caller's list is never mutated
    lo, hi = 0, len(working) - 1  # => the active search range, shrinks each round
    while True:  # => each iteration eliminates one whole side of the partition
        if lo == hi:  # => only one candidate remains -- it must be the answer
            return working[lo]  # => base case: nowhere left to search
        p = random_pivot_partition(working, lo, hi)  # => the pivot's final sorted index
        if p == k:  # => the pivot itself landed exactly at the target rank
            return working[p]  # => found it -- no more recursion needed
        if p < k:  # => the k-th smallest is somewhere to the RIGHT of the pivot
            lo = p + 1  # => discards the entire left side -- it's already too small
        else:  # => the k-th smallest is somewhere to the LEFT of the pivot
            hi = p - 1  # => discards the entire right side -- it's already too big


def random_pivot_partition(
    items: list[int], lo: int, hi: int
) -> int:  # => Lomuto scheme
    rand_index = random.randint(lo, hi)  # => a uniformly random pivot choice
    items[rand_index], items[lo] = items[lo], items[rand_index]  # => moves it to front
    pivot = items[lo]  # => the value being partitioned around
    i = lo  # => boundary of the "<pivot" region
    for j in range(lo + 1, hi + 1):  # => scans the rest of the active range
        if items[j] < pivot:  # => belongs strictly before the pivot
            i += 1  # => grows the "<pivot" region by one slot
            items[i], items[j] = items[j], items[i]  # => swaps it into place
    items[lo], items[i] = items[i], items[lo]  # => places the pivot at its final index
    return i  # => the pivot's final, correctly-sorted-position index


# a fixed seed makes this whole demo fully reproducible across runs
random.seed(17)  # => fixed seed -> reproducible pivot choices
data: list[int] = random.sample(range(1000), 40)  # => 40 distinct random ints
sorted_data = sorted(data)  # => ground truth to check quickselect against
third_smallest = quickselect(data, k=2)  # => 0-indexed: k=2 means the 3rd smallest
median = quickselect(data, k=len(data) // 2)  # => the middle element by rank
print(third_smallest == sorted_data[2])  # => Output: True
print(median == sorted_data[len(data) // 2])  # => Output: True

assert third_smallest == sorted_data[2]  # => confirms rank-2 matches sorted()[2]
assert median == sorted_data[len(data) // 2]  # => confirms the median rank matches too
assert quickselect(data, k=0) == min(data)  # => rank 0 is always the minimum
assert quickselect(data, k=len(data) - 1) == max(data)  # => the last rank is the max
print("ex-28 OK")  # => Output: ex-28 OK
