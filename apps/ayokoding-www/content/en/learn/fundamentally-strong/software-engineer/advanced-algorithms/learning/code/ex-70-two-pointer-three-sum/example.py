"""Example 70: 3-Sum via Sort + Two Pointers -- Unique Triplets, No Duplicates."""

# Fix ONE element, then two-pointer (co-26) the REMAINING sorted array for a
# pair summing to its complement -- exactly Example 23's technique, reused as
# a subroutine. Skipping repeated values at each level is what keeps every
# returned triplet UNIQUE, even when the input itself has many duplicates.


def three_sum(nums: list[int]) -> list[list[int]]:  # => O(n^2): O(n) outer * O(n) inner
    nums_sorted = sorted(
        nums
    )  # => O(n log n): enables both the skip-logic and 2-pointer
    n = len(nums_sorted)
    triplets: list[list[int]] = []  # => accumulates unique triplets summing to zero
    for i in range(n - 2):  # => fixes the FIRST element of each candidate triplet
        if (
            i > 0 and nums_sorted[i] == nums_sorted[i - 1]
        ):  # => same first element as before
            continue  # => SKIPS it -- would only regenerate triplets already found
        lo, hi = i + 1, n - 1  # => two pointers over the REMAINING sorted slice
        target = -nums_sorted[
            i
        ]  # => the pair must sum to exactly this, for a zero total
        while lo < hi:  # => Example 23's exact two-pointer pattern, reused here
            pair_sum = nums_sorted[lo] + nums_sorted[hi]
            if pair_sum == target:  # => found a valid triplet
                triplets.append([nums_sorted[i], nums_sorted[lo], nums_sorted[hi]])
                while (
                    lo < hi and nums_sorted[lo] == nums_sorted[lo + 1]
                ):  # => skip dup lo
                    lo += 1
                while (
                    lo < hi and nums_sorted[hi] == nums_sorted[hi - 1]
                ):  # => skip dup hi
                    hi -= 1
                lo += 1  # => moves past the just-recorded pair
                hi -= 1
            elif pair_sum < target:  # => sum too small -- need a bigger low value
                lo += 1
            else:  # => sum too big -- need a smaller high value
                hi -= 1
    return triplets  # => every unique triplet summing to zero


nums: list[int] = [-1, 0, 1, 2, -1, -4]  # => the classic LeetCode 3-sum example
triplets = three_sum(nums)  # => all unique zero-sum triplets
print(sorted(triplets))  # => Output: [[-1, -1, 2], [-1, 0, 1]]

assert sorted(triplets) == [[-1, -1, 2], [-1, 0, 1]]  # => confirms the known answer
for t in triplets:  # => confirms EVERY triplet genuinely sums to zero
    assert sum(t) == 0
unique_triplets = {tuple(t) for t in triplets}  # => hashable form, catches duplicates
assert len(unique_triplets) == len(triplets)  # => confirms no triplet is repeated
print("ex-70 OK")  # => Output: ex-70 OK
