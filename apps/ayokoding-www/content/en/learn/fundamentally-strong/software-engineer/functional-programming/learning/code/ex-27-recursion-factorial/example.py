"""Example 27: A Recursive Factorial (No TCO)."""

import sys  # => sys.getrecursionlimit -- CPython's hard, load-bearing recursion ceiling


def factorial(n: int) -> int:  # => the textbook recursive definition -- one call per n
    if n <= 1:  # => base case stops the recursion
        return 1  # => factorial(0) and factorial(1) both bottom out here
    return n * factorial(
        n - 1
    )  # => NOT a tail call reduced away -- CPython keeps every frame


result = factorial(10)  # => 10 nested calls deep -- trivially within the default limit
print(result)  # => Output: 3628800

limit = (
    sys.getrecursionlimit()
)  # => the default ceiling (commonly 1000) -- CPython has NO TCO
# => a self-tail-call in Python is NOT collapsed into a loop by the interpreter, unlike Scheme
print(
    limit > 100
)  # => Output: True -- 10 frames of factorial(10) fit comfortably under this
print(10 < limit)  # => Output: True -- confirms this call never approaches the ceiling
