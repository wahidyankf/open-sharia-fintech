"""Example 74: Median-of-Medians Select -- Deterministic O(n) Worst Case."""

# Example 8's naive first-pivot quickselect degrades to O(n^2) on sorted
# input (co-08). Example 27's RANDOM-pivot quickselect fixes that only in
# EXPECTATION -- an adversary who predicts the RNG can still force O(n^2).
# Median-of-medians picks a pivot GUARANTEED to discard a constant fraction
# of the array every call, so worst-case comparisons stay O(n) -- co-01,
# co-08 -- with ZERO dependence on randomness or input order.


def naive_first_pivot_select(arr: list[int], k: int, counter: list[int]) -> int:
    # => the SAME strategy as Example 8: always pivot on arr[0]
    if len(arr) == 1:
        return arr[0]  # => base case: one element left -- it must be the answer
    pivot = arr[0]
    lows: list[int] = []  # => elements strictly less than pivot
    highs: list[int] = []  # => elements strictly greater than pivot
    pivots: list[int] = []  # => elements equal to pivot (handles duplicates)
    for x in arr:
        counter[0] += 1  # => ONE comparison charged per element, per level
        if x < pivot:
            lows.append(x)
        elif x > pivot:
            highs.append(x)
        else:
            pivots.append(x)
    if k < len(lows):
        return naive_first_pivot_select(lows, k, counter)
    if k < len(lows) + len(pivots):
        return pivot  # => k lands inside the pivot-equal group -- done
    return naive_first_pivot_select(
        highs, k - len(lows) - len(pivots), counter
    )  # => recurse into the remainder


def median_of_medians_select(arr: list[int], k: int, counter: list[int]) -> int:
    # => finds the k-th smallest (0-indexed) with a GUARANTEED-good pivot
    if len(arr) <= 5:  # => base case: small enough to sort directly
        counter[0] += len(arr)  # => charges a small, bounded cost for the sort
        return sorted(arr)[k]
    medians: list[int] = []  # => one median per group of (up to) 5 elements
    for i in range(0, len(arr), 5):
        group = sorted(arr[i : i + 5])  # => sorting 5 elements is O(1) work
        counter[0] += len(group)  # => charges that bounded cost
        medians.append(group[len(group) // 2])  # => the middle of each group of 5
    pivot = median_of_medians_select(
        medians, len(medians) // 2, counter
    )  # => recursively finds the MEDIAN OF the medians -- the key trick
    lows: list[int] = []
    highs: list[int] = []
    pivots: list[int] = []
    for x in arr:
        counter[0] += 1  # => ONE comparison charged per element, per level
        if x < pivot:
            lows.append(x)
        elif x > pivot:
            highs.append(x)
        else:
            pivots.append(x)
    # => the median-of-medians pivot is PROVABLY >= 30% and <= 70% of arr,
    # => so recursion always shrinks by at least a constant fraction -- this
    # => is what bounds total work to O(n), unlike Example 8's O(n^2) case
    if k < len(lows):
        return median_of_medians_select(lows, k, counter)
    if k < len(lows) + len(pivots):
        return pivot
    return median_of_medians_select(highs, k - len(lows) - len(pivots), counter)


naive_counter = [0]  # => a single-element list works as a mutable accumulator
mom_counter = [0]
for n in (200, 400):  # => DOUBLING the input size isolates the growth rate
    sorted_input = list(range(n))  # => Example 8's exact adversarial case
    counter = [0]
    naive_first_pivot_select(list(sorted_input), n // 2, counter)
    naive_counter.append(counter[0])  # => records comparisons at this n

    counter = [0]
    median_of_medians_select(list(sorted_input), n // 2, counter)
    mom_counter.append(counter[0])  # => records comparisons at this n

naive_ratio = naive_counter[2] / naive_counter[1]  # => growth from n=200 to n=400
mom_ratio = mom_counter[2] / mom_counter[1]  # => the SAME doubling, for comparison
print(naive_counter[1:])  # => Output: [15150, 60300]
print(mom_counter[1:])  # => Output: [1083, 2299]
print(round(naive_ratio, 1))  # => Output: 4.0 -- doubling n QUADRUPLES the cost
print(round(mom_ratio, 1))  # => Output: 2.1 -- doubling n roughly DOUBLES the cost

assert naive_ratio > 3.5  # => confirms Example 8's naive pivot is QUADRATIC (~4x)
assert mom_ratio < 2.5  # => confirms median-of-medians stays LINEAR (~2x), guaranteed

correctness_input = [37, 2, 91, 15, 4, 68, 23, 5, 100, 12, 44, 8]
for k in range(len(correctness_input)):  # => checks EVERY rank, not just the median
    expected = sorted(correctness_input)[k]  # => the ground-truth k-th smallest
    got = median_of_medians_select(list(correctness_input), k, [0])
    assert got == expected  # => correctness holds regardless of the pivot strategy
print("ex-74 OK")  # => Output: ex-74 OK
