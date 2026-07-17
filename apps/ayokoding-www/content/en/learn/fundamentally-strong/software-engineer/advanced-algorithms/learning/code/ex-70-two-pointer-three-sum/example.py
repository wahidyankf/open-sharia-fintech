"""Example 70: 3-Sum via Sort + Two Pointers -- Unique Triplets, No Duplicates."""

# Fix ONE element, then two-pointer (co-26) the REMAINING sorted array for a
# pair summing to its complement -- exactly Example 23's technique, reused as
# a subroutine. Skipping repeated values at each level is what keeps every
# returned triplet UNIQUE, even when the input itself has many duplicates.


def three_sum(nums: list[int]) -> list[list[int]]:  # => O(n^2): O(n) outer * O(n) inner
    nums_sorted = sorted(  # => opens the sort call
        nums  # => the raw, unsorted input
    )  # => O(n log n): enables both the skip-logic and 2-pointer
    n = len(nums_sorted)  # => the sequence length
    triplets: list[list[int]] = []  # => accumulates unique triplets summing to zero
    for i in range(n - 2):  # => fixes the FIRST element of each candidate triplet
        if (  # => opens the duplicate-first-element check
            i > 0  # => there IS a prior i to compare against
            and nums_sorted[i] == nums_sorted[i - 1]  # => same value as the prior i
        ):  # => same first element as before
            continue  # => SKIPS it -- would only regenerate triplets already found
        lo, hi = i + 1, n - 1  # => two pointers over the REMAINING sorted slice
        target = (  # => opens the target-value negation
            -nums_sorted[  # => opens the target-value lookup
                i  # => the fixed first element's index
            ]
        )  # => the pair must sum to exactly this, for a zero total
        while lo < hi:  # => Example 23's exact two-pointer pattern, reused here
            pair_sum = nums_sorted[lo] + nums_sorted[hi]  # => the current pair's sum
            if pair_sum == target:  # => found a valid triplet
                triplets.append(  # => opens the new-triplet record
                    [nums_sorted[i], nums_sorted[lo], nums_sorted[hi]]
                )  # => records it
                while (  # => opens the skip-duplicate-lo loop
                    lo < hi  # => stays within the shrinking two-pointer range
                    and nums_sorted[lo]
                    == nums_sorted[lo + 1]  # => same lo value repeats
                ):  # => skip dup lo
                    lo += 1  # => advances past the duplicate
                while (  # => opens the skip-duplicate-hi loop
                    lo < hi  # => stays within the shrinking two-pointer range
                    and nums_sorted[hi]
                    == nums_sorted[hi - 1]  # => same hi value repeats
                ):  # => skip dup hi
                    hi -= 1  # => advances past the duplicate
                lo += 1  # => moves past the just-recorded pair
                hi -= 1  # => moves past the just-recorded pair on the other side
            elif pair_sum < target:  # => sum too small -- need a bigger low value
                lo += 1  # => shrinks the range from the left
            else:  # => sum too big -- need a smaller high value
                hi -= 1  # => shrinks the range from the right
    return triplets  # => every unique triplet summing to zero


# => the classic LeetCode 3-sum example, with duplicate -1's to exercise the skip-logic
nums: list[int] = [-1, 0, 1, 2, -1, -4]  # => the classic LeetCode 3-sum example
triplets = three_sum(nums)  # => all unique zero-sum triplets
print(sorted(triplets))  # => Output: [[-1, -1, 2], [-1, 0, 1]]

assert sorted(triplets) == [[-1, -1, 2], [-1, 0, 1]]  # => confirms the known answer
for t in triplets:  # => confirms EVERY triplet genuinely sums to zero
    assert sum(t) == 0  # => this triplet's own three values sum to exactly 0
unique_triplets = {tuple(t) for t in triplets}  # => hashable form, catches duplicates
assert len(unique_triplets) == len(triplets)  # => confirms no triplet is repeated
print("ex-70 OK")  # => Output: ex-70 OK
