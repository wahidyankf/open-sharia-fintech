"""Example 76: Reducing Subset-Sum to Partition -- a Concrete NP-Hardness Proof Sketch."""

# A REDUCTION proves problem B is at least as hard as problem A by turning
# any A-instance into a B-instance that has the SAME yes/no answer (co-28).
# Here, Subset-Sum(items, target) reduces to Partition(items'): add ONE
# padding element so "some subset sums to target" becomes EXACTLY "this new
# set splits into two equal-sum halves." This is the textbook proof that
# Partition is NP-hard, GIVEN that Subset-Sum is already known NP-hard.


def subset_sum_possible(
    items: list[int], target: int
) -> bool:  # => the SOURCE problem: is `target` reachable by summing a subset?
    if target < 0:
        return False
    achievable: set[int] = {0}  # => 0 is always reachable (the empty subset)
    for x in items:
        newly_reachable: set[int] = set()
        for s in achievable:
            if s + x <= target:  # => prunes sums that overshoot the target
                newly_reachable.add(s + x)
        achievable |= newly_reachable  # => grows the set of reachable sums
    return target in achievable


def can_partition(
    items: list[int],
) -> bool:  # => the TARGET problem: two equal-sum halves?
    total = sum(items)
    if total % 2 != 0:  # => an odd total can NEVER split into two equal integer halves
        return False
    return subset_sum_possible(
        items, total // 2
    )  # => Partition IS Subset-Sum with target = total/2 -- the "obvious" direction


def reduce_subset_sum_to_partition(
    items: list[int], target: int
) -> list[int]:  # => THE REDUCTION: builds a Partition instance from a Subset-Sum one
    total = sum(items)
    padding = total - 2 * target  # => the single new element that makes the trick work
    assert padding >= 0, (
        "reduction requires target <= total / 2"
    )  # => a documented precondition
    # => algebra: if some A subseteq items sums to `target`, then
    # => (items \ A) sums to (total - target), and (A + [padding]) ALSO sums
    # => to (target + padding) = (total - target) -- an EXACT equal split
    return items + [padding]


items = [3, 7, 2, 9, 5]
total = sum(items)  # => 26
half = total // 2  # => 13 -- the largest valid target for this reduction

mismatches = 0
for target in range(half + 1):  # => sweeps EVERY possible target from 0 to half
    direct_answer = subset_sum_possible(items, target)  # => the SOURCE problem's answer
    reduced_instance = reduce_subset_sum_to_partition(items, target)
    reduced_answer = can_partition(reduced_instance)  # => the TARGET problem's answer
    if direct_answer != reduced_answer:
        mismatches += 1  # => would indicate the reduction is BROKEN

print(mismatches)  # => Output: 0 -- every target's answer survives the reduction
print(subset_sum_possible(items, 12))  # => Output: True -- e.g. {7, 5} sums to 12
print(
    can_partition(reduce_subset_sum_to_partition(items, 12))
)  # => Output: True -- matches
print(subset_sum_possible(items, 1))  # => Output: False -- no subset sums to 1
print(
    can_partition(reduce_subset_sum_to_partition(items, 1))
)  # => Output: False -- matches

assert (
    mismatches == 0
)  # => confirms the reduction preserves EVERY yes/no answer, not just one
assert (
    len(reduce_subset_sum_to_partition(items, 12)) == len(items) + 1
)  # => adds exactly 1 element
print("ex-76 OK")  # => Output: ex-76 OK
