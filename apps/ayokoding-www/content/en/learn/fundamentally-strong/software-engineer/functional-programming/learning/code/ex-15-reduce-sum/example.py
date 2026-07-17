"""Example 15: reduce() Sums a List."""

from functools import reduce  # => reduce lives in functools, not the builtins


def add(
    a: int, b: int
) -> int:  # => the "how to combine two values" step reduce repeats
    return a + b  # => the two-argument combiner reduce calls at every step


nums = [1, 2, 3, 4, 5]  # => the source sequence

total = reduce(add, nums, 0)  # => folds nums into ONE value, starting from the seed 0
# => reduce computes add(add(add(add(add(0,1),2),3),4),5) -- one running accumulator, no loop written

print(total)  # => Output: 15
print(
    total == sum(nums)
)  # => Output: True -- reduce(add, ..., 0) IS how sum() works internally
