"""Example 22: Slice List."""

nums: list[int] = [0, 1, 2, 3, 4]  # => nums is [0, 1, 2, 3, 4] (type: list[int])
# Slicing never mutates nums -- each print below returns a brand-new list.
print(nums[1:4])  # => [start:stop] -- indices 1, 2, 3 (stop is exclusive) -- [1, 2, 3]
print(nums[::-1])  # => a step of -1 walks the whole list backward -- [4, 3, 2, 1, 0]
