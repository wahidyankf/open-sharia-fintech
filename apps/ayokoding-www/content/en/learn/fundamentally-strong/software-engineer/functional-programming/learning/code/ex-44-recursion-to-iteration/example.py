"""Example 44: Converting Deep Recursion to an Explicit Stack."""

import sys  # => sys.getrecursionlimit reveals the current recursion ceiling


def sum_to_n_recursive(
    n: int,
) -> int:  # => the natural recursive definition -- one frame per call
    if n == 0:  # => base case: nothing left to add
        return 0  # => the base case's value
    return n + sum_to_n_recursive(
        n - 1
    )  # => grows the call stack by exactly one frame per call


def sum_to_n_iterative(
    n: int,
) -> int:  # => the SAME computation, an explicit stack instead of the call stack
    stack: list[int] = list(
        range(1, n + 1)
    )  # => an explicit, heap-allocated stack -- NOT the call stack
    total = 0  # => the running total, mutated below
    while (
        stack
    ):  # => pops until the explicit stack is empty -- no Python call frames grow
        total += (
            stack.pop()
        )  # => pops one value at a time -- heap memory, not call-stack frames
    return total  # => the final total after the explicit stack empties


deep_n = sys.getrecursionlimit() + 500  # => deliberately EXCEEDS the recursion ceiling

try:  # => opens a block that expects the recursive call below to raise
    sum_to_n_recursive(deep_n)  # => this call is expected to blow the call stack
    recursive_raised = False  # => unreachable if RecursionError fires as expected
except RecursionError:  # => confirms the exact failure recursion has at this depth
    recursive_raised = True  # => confirms the recursive version genuinely failed here

iterative_result = sum_to_n_iterative(
    deep_n
)  # => the SAME depth, but no call-stack growth at all

# => CPython has NO tail-call optimization -- deep recursion genuinely can crash
print(
    recursive_raised
)  # => Output: True -- the recursive version genuinely fails at this depth
print(
    iterative_result == deep_n * (deep_n + 1) // 2
)  # => Output: True -- the iterative version succeeds
