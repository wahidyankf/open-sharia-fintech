"""Example 14: Higher-Order Map."""

from collections.abc import Callable


def apply_all(fn: Callable[[int], int], items: list[int]) -> list[int]:  # => fn is an ORDINARY parameter
    return [fn(item) for item in items]  # => the function passed in gets called once per item
    # => apply_all doesn't know or care WHAT fn does -- it only knows fn's shape: int -> int


def double(n: int) -> int:  # => one possible function-as-value to pass in
    return n * 2  # => doubles its argument


def square(n: int) -> int:  # => a second, unrelated function-as-value
    return n * n  # => squares its argument


numbers: list[int] = [1, 2, 3, 4]  # => shared input list
print(apply_all(double, numbers))  # => passing `double` itself, not calling it, as an argument
# => Output: [2, 4, 6, 8]
print(apply_all(square, numbers))  # => same apply_all, DIFFERENT behavior -- just by swapping the function
# => Output: [1, 4, 9, 16]
print(apply_all(lambda n: n + 100, numbers))  # => a function value can be anonymous too
# => Output: [101, 102, 103, 104]
