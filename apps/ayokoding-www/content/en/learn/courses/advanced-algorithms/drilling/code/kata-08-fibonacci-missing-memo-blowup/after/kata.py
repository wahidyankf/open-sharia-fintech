"""Kata 8 (after): memoization caches each subproblem's result, so it is only ever solved ONCE."""

calls = 0
cache: dict[int, int] = {}


def fib(n: int) -> int:
    global calls
    calls += 1
    if (
        n in cache
    ):  # => already solved this exact subproblem -- reuse it instead of re-recursing
        return cache[n]
    if n <= 1:
        return n
    result = fib(n - 1) + fib(n - 2)
    cache[n] = result
    return result


result = fib(25)
print(result)
print(calls)
print(calls <= 2 * 25 + 1)  # memoized fib(25) makes O(n) calls -- 49, not 242,785
