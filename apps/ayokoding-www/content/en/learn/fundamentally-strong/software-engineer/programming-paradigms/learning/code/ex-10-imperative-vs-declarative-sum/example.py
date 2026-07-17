"""Example 10: Imperative vs Declarative Sum."""


def sum_of_squares_of_evens_imperative(nums: list[int]) -> int:  # => HOW: explicit accumulator loop
    total = 0  # => mutable running total, starts at zero
    for n in nums:  # => explicit iteration
        if n % 2 == 0:  # => explicit filter check
            total += n * n  # => explicit mutate-in-place accumulation
    return total  # => the final value of the mutated box


def sum_of_squares_of_evens_declarative(nums: list[int]) -> int:  # => WHAT: one expression, no box
    return sum(n * n for n in nums if n % 2 == 0)  # => "the sum of squares of the evens", read as English
    # => sum() consumes a generator expression -- no named accumulator variable exists anywhere


data: list[int] = list(range(1, 11))  # => 1 through 10, same input shape as example 9
how_result = sum_of_squares_of_evens_imperative(data)  # => 2^2+4^2+6^2+8^2+10^2 = 4+16+36+64+100=220
what_result = sum_of_squares_of_evens_declarative(data)  # => must compute the identical integer
print(how_result)  # => the imperative total
# => Output: 220
print(how_result == what_result)  # => confirms both styles agree on the final integer
# => Output: True
