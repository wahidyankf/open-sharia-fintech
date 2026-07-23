"""Example 82: Convert Deep Recursion to Iteration to Avoid RecursionError."""

import sys  # => used to read the current recursion-depth ceiling


# Recurses n deep -- one call-stack frame per level (co-17).
def sum_to_n_recursive(n: int) -> int:  # => a plain recursive function
    if n == 0:  # => BASE CASE
        return 0  # => the additive identity, so the recursion can bottom out
    return n + sum_to_n_recursive(
        n - 1
    )  # => RECURSIVE CASE -- consumes a stack frame each call


# Same result, but a plain loop uses O(1) call-stack frames regardless of n (co-18).
def sum_to_n_iterative(n: int) -> int:  # => a plain iterative function
    total = 0  # => all state lives in local variables, not in nested call frames
    for i in range(n + 1):  # => a single frame handles EVERY value of i
        total += i  # => accumulates the running sum
    return total  # => the final sum from 0 through n


small_recursive = sum_to_n_recursive(100)  # => well within the default recursion limit
small_iterative = sum_to_n_iterative(100)  # => same answer, no recursion at all
print(small_recursive, small_iterative)  # => Output: 5050 5050
assert small_recursive == small_iterative == 5050  # => confirms both approaches agree

limit = sys.getrecursionlimit()  # => CPython's default call-stack depth ceiling
try:
    sum_to_n_recursive(
        limit + 1000
    )  # => deliberately exceeds the limit -- should raise
    raised = False  # => not reached -- the call above is expected to raise first
except RecursionError:  # => RecursionError is a RuntimeError subclass (co-18)
    raised = True  # => confirms the deep recursive version genuinely fails at depth

large_iterative = sum_to_n_iterative(
    limit + 1000
)  # => the SAME large n, iteratively -- succeeds
print(raised)  # => Output: True
print(large_iterative > 0)  # => Output: True

assert raised is True  # => confirms recursion alone cannot handle this depth
assert (
    large_iterative == (limit + 1000) * (limit + 1001) // 2
)  # => Gauss's sum formula, cross-check
print("ex-82 OK")  # => Output: ex-82 OK
