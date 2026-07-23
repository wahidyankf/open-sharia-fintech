"""Example 15: List Index Mutate."""

nums: list[int] = [1, 2, 3]  # => nums is [1, 2, 3] (type: list[int])
# Lists are mutable -- index assignment changes the list in place, no new list created.
nums[0] = 9  # => index assignment replaces the element in place -- lists are mutable
print(nums)  # => Output: [9, 2, 3]
