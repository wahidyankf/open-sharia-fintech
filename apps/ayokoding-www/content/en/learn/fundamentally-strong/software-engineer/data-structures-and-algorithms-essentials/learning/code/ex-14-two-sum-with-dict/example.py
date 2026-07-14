"""Example 14: Two Sum, Solved with a Dict."""


# Returns indices (i, j) where nums[i] + nums[j] == target, in one O(n) pass (co-08).
def two_sum(nums: list[int], target: int) -> tuple[int, int]:  # => a plain function
    seen: dict[int, int] = {}  # => maps "value already seen" -> "its index"
    for index, value in enumerate(nums):  # => walks nums once, tracking position
        complement = target - value  # => the value that would complete the pair
        if complement in seen:  # => O(1) average check -- no nested loop needed
            return seen[complement], index  # => found: earlier index, current index
        seen[value] = index  # => remember this value's index for a LATER complement
    raise ValueError("no two sum solution")  # => every input in this example has one


indices = two_sum([2, 7, 11, 15], 9)  # => 2 (index 0) + 7 (index 1) == 9
print(indices)  # => Output: (0, 1)

assert indices == (0, 1)  # => confirms the two indices sum to the target value
assert two_sum([3, 2, 4], 6) == (1, 2)  # => confirms a second fixture also resolves
print("ex-14 OK")  # => Output: ex-14 OK
