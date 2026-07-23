"""Example 14: List Basics."""

nums: list[int] = [1, 2, 3]  # => a mutable, ordered sequence literal
nums.append(4)  # => appends in place -- no reassignment needed
print(nums)  # => Output: [1, 2, 3, 4]
