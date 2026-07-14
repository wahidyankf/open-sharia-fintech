"""Example 76: Two-Pointer Pair Sum on a Sorted Array."""


# On SORTED data, two pointers closing inward solve this in O(n) --
# no nested loop and no dict needed, unlike Example 14's unsorted version (co-20, co-14).
def pair_sum(
    sorted_values: list[int], target: int
) -> tuple[int, int]:  # => two-pointer scan
    left, right = 0, len(sorted_values) - 1  # => start at both ends of the sorted range
    while (
        left < right
    ):  # => the pointers move strictly toward each other, O(n) total steps
        current_sum = (
            sorted_values[left] + sorted_values[right]
        )  # => the pair's current sum
        if current_sum == target:  # => an exact match
            return left, right  # => found -- return immediately
        if (
            current_sum < target
        ):  # => sum too small -- the only way to grow it is a bigger left
            left += 1  # => sorted order guarantees this strictly increases current_sum
        else:  # => sum too large -- the only way to shrink it is a smaller right
            right -= 1  # => sorted order guarantees this strictly decreases current_sum
    raise ValueError("no pair sums to target")  # => not hit in this example


sorted_values = [
    1,
    2,
    4,
    6,
    8,
    11,
]  # => must already be sorted for the two pointers to work
indices = pair_sum(
    sorted_values, 10
)  # => sorted_values[1] + sorted_values[4] == 2 + 8 == 10
print(indices)  # => Output: (1, 4)

assert indices == (1, 4)  # => confirms the exact pair of indices found
assert (
    sorted_values[indices[0]] + sorted_values[indices[1]] == 10
)  # => confirms the sum itself
print("ex-76 OK")  # => Output: ex-76 OK
