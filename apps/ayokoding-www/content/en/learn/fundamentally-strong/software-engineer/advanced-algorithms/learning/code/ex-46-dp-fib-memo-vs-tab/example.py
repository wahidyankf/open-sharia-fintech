"""Example 46: Fibonacci -- Top-Down Memoization vs Bottom-Up Tabulation."""

# Both DP styles (co-23) exploit OVERLAPPING SUBPROBLEMS -- naive recursive
# fib(n) recomputes fib(5) exponentially many times. Memoization caches
# top-down recursive results; tabulation builds the answer bottom-up in a
# loop, with no recursion (and no call-stack depth risk) at all.


def fib_memo(n: int, cache: dict[int, int] | None = None) -> int:  # => top-down, cached
    if cache is None:  # => the first call creates a fresh cache -- never share defaults
        cache = {}  # => a new, empty memo for this top-level call
    if n <= 1:  # => base cases: fib(0)=0, fib(1)=1
        return n  # => no recursion needed at the base
    if n in cache:  # => already computed -- an O(1) cache hit
        return cache[n]  # => reuses the previously computed result
    cache[n] = fib_memo(n - 1, cache) + fib_memo(
        n - 2, cache
    )  # => computes ONCE, caches
    return cache[n]  # => the newly computed and cached value


def fib_tab(n: int) -> int:  # => bottom-up, iterative, no recursion at all
    if n <= 1:  # => base cases, same as above
        return n
    prev2, prev1 = 0, 1  # => fib(0) and fib(1), the two seeds tabulation builds from
    for _ in range(2, n + 1):  # => builds each fib(i) from the two before it
        prev2, prev1 = prev1, prev2 + prev1  # => slides the window forward by one
    return prev1  # => fib(n), built up with O(1) extra space, no call stack at all


values: list[int] = [0, 1, 5, 10, 20, 30]  # => a spread of inputs, including base cases
memo_results = [fib_memo(n) for n in values]  # => top-down answers
tab_results = [fib_tab(n) for n in values]  # => bottom-up answers
print(memo_results)  # => Output: [0, 1, 5, 55, 6765, 832040]
print(tab_results)  # => Output: [0, 1, 5, 55, 6765, 832040]

assert memo_results == tab_results  # => confirms both styles agree on every input
assert fib_tab(30) == 832040  # => confirms a specific known Fibonacci value
print("ex-46 OK")  # => Output: ex-46 OK
