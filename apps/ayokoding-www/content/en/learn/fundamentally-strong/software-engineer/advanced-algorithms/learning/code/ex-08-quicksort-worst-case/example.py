"""Example 8: Naive First-Pivot Quicksort's O(n^2) Blow-Up on Sorted Input."""

# A naive quicksort that always picks the FIRST element as pivot degrades to
# O(n^2) on already-sorted input (co-08, co-01): every partition splits into
# "0 elements <= pivot" and "n-1 elements > pivot" -- the worst possible split.

comparisons = 0  # => a global counter -- counts every pivot comparison made


def naive_quicksort(  # => sorts items in place between indices lo and hi inclusive
    items: list[int], lo: int = 0, hi: int | None = None
) -> None:  # => returns nothing -- mutates items directly
    global comparisons  # => this function mutates the module-level counter
    if hi is None:  # => top-level call defaults hi to the last index
        hi = len(items) - 1  # => sorts the WHOLE list on the first call
    if lo < hi:  # => base case: 0 or 1 elements need no partitioning
        p = first_pivot_partition(items, lo, hi)  # => partitions around items[lo]
        naive_quicksort(items, lo, p - 1)  # => recurses on the left partition
        naive_quicksort(items, p + 1, hi)  # => recurses on the right partition


def first_pivot_partition(  # => partitions items[lo..hi] around items[lo]
    items: list[int], lo: int, hi: int
) -> int:  # => returns the pivot's final resting index
    global comparisons  # => mutates the shared counter
    pivot = items[lo]  # => THE NAIVE CHOICE: always the first element, never randomized
    i = lo  # => boundary of the "<pivot" region
    for j in range(lo + 1, hi + 1):  # => scans every element after the pivot
        comparisons += 1  # => counts this one comparison against the pivot
        if items[j] < pivot:  # => belongs strictly before the pivot
            i += 1  # => grows the "<pivot" region
            items[i], items[j] = items[j], items[i]  # => swaps it in
    items[lo], items[i] = items[i], items[lo]  # => places the pivot at its final spot
    return i  # => pivot's final index


already_sorted: list[int] = list(range(200))  # => THE WORST CASE: input is pre-sorted
naive_quicksort(already_sorted)  # => sorts in place, counting comparisons as it goes
n = len(already_sorted)  # => n = 200
predicted_worst_case = n * (n - 1) // 2  # => the exact O(n^2) worst-case formula
print(comparisons)  # => Output: 19900
print(predicted_worst_case)  # => Output: 19900

assert (  # => opens the check -- wraps the long boolean across two lines
    comparisons == predicted_worst_case  # => True only if the blow-up was exact
)  # => confirms the empirical count matches the O(n^2) formula EXACTLY
assert already_sorted == list(  # => opens the second check on final correctness
    range(200)  # => rebuilds the original 0..199 sequence for comparison
)  # => confirms the (slow) sort was still correct
print("ex-08 OK")  # => Output: ex-08 OK
