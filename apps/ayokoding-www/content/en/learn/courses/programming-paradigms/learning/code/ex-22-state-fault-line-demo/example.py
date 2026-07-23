"""Example 22: State Fault Line Demo."""

from functools import reduce

running_total: int = 0  # => MUTABLE GLOBAL: state lives outside any function, anyone can touch it


def add_mutable(n: int) -> None:  # => mutates the module-level global -- state lives "out there"
    global running_total  # => explicit acknowledgement that this reaches outside the function
    running_total += n  # => the ONLY line in this file that mutates shared state


def total_immutable(nums: list[int]) -> int:  # => an IMMUTABLE FOLD -- state lives only inside the call
    return reduce(lambda acc, n: acc + n, nums, 0)  # => each step's `acc` is a fresh value, never mutated
    # => no global exists here at all -- the running total is just a local parameter that gets replaced


numbers = [10, 20, 30]  # => shared input for both styles
for n in numbers:  # => drive the mutable-global version
    add_mutable(n)  # => each call reaches OUT to touch shared module state
print(running_total)  # => 10 + 20 + 30, accumulated via repeated mutation of a global
# => Output: 60

fold_result = total_immutable(numbers)  # => drive the immutable-fold version, one call, no mutation
print(fold_result)  # => must compute the identical total, with no state living outside the call
# => Output: 60
print(running_total == fold_result)  # => both styles count the same thing -- they differ in WHERE state lives
# => Output: True
