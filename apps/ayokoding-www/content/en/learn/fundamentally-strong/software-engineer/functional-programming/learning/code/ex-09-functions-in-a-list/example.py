"""Example 9: Functions Stored in a List."""


def double(x: int) -> int:  # => three ordinary, unrelated single-purpose functions
    return x * 2  # => doubles its argument


def square(x: int) -> int:
    return x * x  # => squares its argument


def negate(x: int) -> int:
    return -x  # => flips the sign of its argument


operations = [
    double,
    square,
    negate,
]  # => a list of FUNCTION OBJECTS, not their results
# => nothing has been called yet -- the list just holds three callables

results = [
    op(5) for op in operations
]  # => calls each stored function with the same input
# => results is [10, 25, -5]: double(5), square(5), negate(5) in that order

print(results)  # => Output: [10, 25, -5]
print(
    all(callable(op) for op in operations)
)  # => Output: True -- every element is callable
