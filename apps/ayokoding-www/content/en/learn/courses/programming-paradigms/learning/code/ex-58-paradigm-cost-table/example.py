"""Example 58: Paradigm Cost Table."""

import inspect  # => inspect.getsource() reads a function's own source text, used by count_lines() below
from collections.abc import Callable  # => types the plain-function argument shared by both metric helpers below


def evens_squared_imperative(nums: list[int]) -> list[int]:  # => same task as example 9, measured here
    result: list[int] = []  # => mutable accumulator -- one extra local name declarative avoids
    for n in nums:  # => explicit iteration over every input number
        if n % 2 == 0:  # => explicit selection: keep only even numbers
            result.append(n * n)  # => explicit mutate-in-place append of the squared value
    return result  # => the fully built accumulator


def evens_squared_declarative(nums: list[int]) -> list[int]:  # => the declarative twin, measured here too
    return [n * n for n in nums if n % 2 == 0]  # => the same result, no named accumulator anywhere


def count_lines(fn: Callable[..., object]) -> int:  # => a concrete, reproducible metric: physical lines of the function's body
    return len(inspect.getsource(fn).strip().splitlines())  # => counts every line, def line included


def count_local_names(fn: Callable[..., object]) -> int:  # => a second concrete metric: how many local variable names the body binds
    code = fn.__code__  # => plain functions always carry __code__, pyright resolves it on Callable[..., object]
    return code.co_nlocals - len(code.co_varnames[: code.co_argcount])  # => locals minus params
    # => co_nlocals counts every local slot; subtracting the parameters leaves ONLY the names the body itself
    # => introduces -- both versions need the loop variable `n`, but only imperative ALSO needs a separate
    # => named accumulator (`result`) to collect results across iterations, one extra name declarative avoids


rows: list[tuple[str, int, int]] = [  # => the comparison table, built from ACTUAL measurements, not opinion
    ("imperative", count_lines(evens_squared_imperative), count_local_names(evens_squared_imperative)),  # => row 1
    ("declarative", count_lines(evens_squared_declarative), count_local_names(evens_squared_declarative)),  # => row 2
]  # => closes the measured comparison table

for name, lines, local_names in rows:  # => print the table, one row per paradigm
    print(f"{name}: lines={lines} local_names={local_names}")  # => the measured numbers, not an opinion
# => Output: imperative: lines=6 local_names=2
# => Output: declarative: lines=2 local_names=1

same_result = evens_squared_imperative([1, 2, 3, 4]) == evens_squared_declarative([1, 2, 3, 4])  # => equivalence check
print(same_result)  # => the cost comparison is only meaningful because both versions are provably equivalent
# => Output: True
