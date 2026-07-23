"""Example 35: Define Typed Function."""


# `-> int` annotates the RETURN type, checked statically by pyright.
def add(a: int, b: int) -> int:  # => defines add, takes two ints, returns an int
    return a + b  # => returns the sum of a and b


print(add(2, 3))  # => Output: 5
