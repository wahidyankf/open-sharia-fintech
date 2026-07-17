"""Example 67: Imperative-to-Functional Refactor."""

from functools import reduce  # => reduce() powers the AFTER version's two folds below


def running_max_and_sum_mutation_heavy(nums: list[int]) -> tuple[int, int]:  # => BEFORE: mutates its own input
    total = 0  # => mutable accumulator #1
    best = nums[0]  # => mutable accumulator #2
    for i in range(len(nums)):  # => manual indexing
        nums[i] = nums[i] + 1  # => MUTATES THE CALLER'S LIST IN PLACE -- a hidden side effect
        total += nums[i]  # => second mutable accumulator update, tangled with the mutation above
        if nums[i] > best:  # => manual running-max check, interleaved with the sum
            best = nums[i]  # => mutates `best` in place -- three concerns tangled in one loop body
    return total, best  # => the caller's list is now silently different from what they passed in


def running_max_and_sum_pure_fold(nums: tuple[int, ...]) -> tuple[int, int]:  # => AFTER: a pure fold
    bumped = tuple(n + 1 for n in nums)  # => a NEW tuple, original untouched
    total = reduce(lambda acc, n: acc + n, bumped, 0)  # => fold #1: sum
    best = reduce(lambda acc, n: max(acc, n), bumped, bumped[0])  # => fold #2: max
    return total, best  # => identical answer, but the input is provably never mutated


mutable_input = [1, 2, 3]  # => list, so the BEFORE version's mutation is possible
before_result = running_max_and_sum_mutation_heavy(mutable_input)  # => call the mutation-heavy version
print(mutable_input)  # => THE BUG: the caller's list was silently mutated
# => Output: [2, 3, 4]

immutable_input = (1, 2, 3)  # => the SAME original values, but as a tuple this time
after_result = running_max_and_sum_pure_fold(immutable_input)  # => call the pure version
print(immutable_input)  # => provably unchanged
# => Output: (1, 2, 3)
print(before_result == after_result)  # => same computed answer despite the different mutation behavior
# => Output: True
