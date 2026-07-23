"""Example 23: Two Pointers -- Find a Pair Summing to Target in O(n)."""

# On a SORTED array, two pointers (co-26) starting at each end can find a
# target-sum pair in one O(n) pass: if the sum is too small, the low pointer
# is too conservative (move it right); too big, the high pointer is (move left).


def two_pointer_pair_sum(
    sorted_items: list[int], target: int
) -> tuple[int, int] | None:  # => returns a pair of (value, value) or None
    lo = 0  # => starts at the smallest element
    hi = len(sorted_items) - 1  # => starts at the largest element
    while lo < hi:  # => stops once the pointers meet -- every pair has been considered
        current_sum = sorted_items[lo] + sorted_items[hi]  # => the pair's current sum
        if current_sum == target:  # => found an exact match
            return (sorted_items[lo], sorted_items[hi])  # => the matching pair
        if current_sum < target:  # => sum too small -- need a bigger low value
            lo += 1  # => moves lo rightward, toward larger values
        else:  # => sum too big -- need a smaller high value
            hi -= 1  # => moves hi leftward, toward smaller values
    return None  # => the pointers crossed without ever matching target


data: list[int] = [1, 3, 4, 7, 9, 12, 15]  # => already sorted, ascending
result = two_pointer_pair_sum(data, target=11)  # => needs SEVERAL pointer moves to find
print(result)  # => Output: (4, 7)
missing = two_pointer_pair_sum(data, target=100)  # => no pair sums to 100
print(missing)  # => Output: None

assert result is not None  # => narrows the type for the sum check below
assert sum(result) == 11  # => confirms the returned pair really sums to the target
assert missing is None  # => confirms an unreachable target correctly returns None
print("ex-23 OK")  # => Output: ex-23 OK
