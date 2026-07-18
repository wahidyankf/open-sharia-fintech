"""Example 76: Reducing Subset-Sum to Partition -- a Concrete NP-Hardness Proof Sketch."""

# A REDUCTION proves problem B is at least as hard as problem A by turning
# any A-instance into a B-instance that has the SAME yes/no answer (co-28).
# Here, Subset-Sum(items, target) reduces to Partition(items'): add ONE
# padding element so "some subset sums to target" becomes EXACTLY "this new
# set splits into two equal-sum halves." This is the textbook proof that
# Partition is NP-hard, GIVEN that Subset-Sum is already known NP-hard.


def subset_sum_possible(  # => tracks the growing set of reachable sums, level by level
    items: list[int],  # => the candidate items to sum a subset of
    target: int,  # => the candidate items and the sum to test for
) -> bool:  # => the SOURCE problem: is `target` reachable by summing a subset?
    if target < 0:  # => a negative target is never reachable by non-negative sums
        return False  # => trivially unreachable
    achievable: set[int] = {0}  # => 0 is always reachable (the empty subset)
    for x in items:  # => processes each item once, growing the reachable-sums set
        newly_reachable: set[int] = set()  # => sums discovered by adding x this round
        for s in achievable:  # => tries adding x to every sum reachable so far
            if s + x <= target:  # => prunes sums that overshoot the target
                newly_reachable.add(s + x)  # => a new reachable sum
        achievable |= newly_reachable  # => grows the set of reachable sums
    return target in achievable  # => True iff some subset sums to exactly target


def can_partition(  # => reduces to Subset-Sum with target = half the total
    items: list[int],  # => the items to try splitting into two equal-sum halves
) -> bool:  # => the TARGET problem: two equal-sum halves?
    total = sum(items)  # => the whole set's total sum
    if total % 2 != 0:  # => an odd total can NEVER split into two equal integer halves
        return False  # => immediately impossible
    return subset_sum_possible(  # => opens the delegated Subset-Sum call
        items,  # => the same items, unchanged
        total // 2,  # => the same items, targeting exactly half the total
    )  # => Partition IS Subset-Sum with target = total/2 -- the "obvious" direction


def reduce_subset_sum_to_partition(  # => builds one padding element that makes the reduction exact
    items: list[int],  # => the original Subset-Sum instance's items
    target: int,  # => the Subset-Sum instance being reduced
) -> list[int]:  # => THE REDUCTION: builds a Partition instance from a Subset-Sum one
    total = sum(items)  # => the original items' total sum
    padding = total - 2 * target  # => the single new element that makes the trick work
    assert padding >= 0, (  # => opens the precondition assertion
        "reduction requires target <= total / 2"  # => the documented message if it fails
    )  # => a documented precondition
    # => algebra: if some A subseteq items sums to `target`, then
    # => (items \ A) sums to (total - target), and (A + [padding]) ALSO sums
    # => to (target + padding) = (total - target) -- an EXACT equal split
    return items + [padding]  # => the constructed Partition instance


items = [3, 7, 2, 9, 5]  # => a small, arbitrary Subset-Sum instance
total = sum(items)  # => 26
half = total // 2  # => 13 -- the largest valid target for this reduction

mismatches = 0  # => counts any target where the reduction's answer disagrees
for target in range(half + 1):  # => sweeps EVERY possible target from 0 to half
    direct_answer = subset_sum_possible(items, target)  # => the SOURCE problem's answer
    reduced_instance = reduce_subset_sum_to_partition(  # => opens the reduction call
        items, target
    )  # => builds the reduced instance
    reduced_answer = can_partition(reduced_instance)  # => the TARGET problem's answer
    if direct_answer != reduced_answer:  # => the two answers should ALWAYS agree
        mismatches += 1  # => would indicate the reduction is BROKEN

print(mismatches)  # => Output: 0 -- every target's answer survives the reduction
print(subset_sum_possible(items, 12))  # => Output: True -- e.g. {7, 5} sums to 12
print(  # => opens the reduced-instance-12 print call
    can_partition(  # => the TARGET problem, applied to the reduced instance
        reduce_subset_sum_to_partition(items, 12)
    )  # => TARGET problem's answer
)  # => Output: True -- matches
print(subset_sum_possible(items, 1))  # => Output: False -- no subset sums to 1
print(  # => opens the reduced-instance-1 print call
    can_partition(  # => the TARGET problem, applied to the reduced instance
        reduce_subset_sum_to_partition(items, 1)
    )  # => TARGET problem's answer
)  # => Output: False -- matches

assert (  # => opens the zero-mismatches sanity check
    mismatches == 0  # => every single target agreed between the two problems
)  # => confirms the reduction preserves EVERY yes/no answer, not just one
assert (  # => opens the exactly-one-padding-element check
    len(reduce_subset_sum_to_partition(items, 12))
    == len(items) + 1  # => exactly one padding element
)  # => adds exactly 1 element
print("ex-76 OK")  # => Output: ex-76 OK
