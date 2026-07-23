"""Example 9: Declarative Comprehension."""

numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # => shared input for both versions


def evens_squared_imperative(nums: list[int]) -> list[int]:  # => HOW: explicit loop + append
    result: list[int] = []  # => mutable accumulator we must remember to build up
    for n in nums:  # => step through every number
        if n % 2 == 0:  # => explicit filter check
            result.append(n * n)  # => explicit transform-and-store step
    return result  # => hand back the accumulator


def evens_squared_declarative(nums: list[int]) -> list[int]:  # => WHAT: state the shape of the result
    return [n * n for n in nums if n % 2 == 0]  # => "the squares of the evens" -- no loop mechanics
    # => filter (if n % 2 == 0) and transform (n * n) read left to right, like the English description


imperative_result = evens_squared_imperative(numbers)  # => run the HOW version
declarative_result = evens_squared_declarative(numbers)  # => run the WHAT version
print(imperative_result)  # => both versions must agree on the values
# => Output: [4, 16, 36, 64, 100]
print(imperative_result == declarative_result)  # => confirms identical lists, same order
# => Output: True
