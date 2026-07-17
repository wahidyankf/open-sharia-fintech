"""Example 78: Paradigm Portfolio README."""

from dataclasses import dataclass  # => @dataclass generates MatrixRow's __init__ from its three fields
from functools import reduce  # => powers the functional solution's fold below


def evens_squared_imperative(nums: list[int]) -> list[int]:  # => the SAME task, solved four ways below
    result: list[int] = []  # => mutable accumulator -- imperative style's defining trait
    for n in nums:  # => manual iteration
        if n % 2 == 0:  # => manual filter check
            result.append(n * n)  # => manual mutation, one element at a time
    return result  # => the accumulated result


class EvensSquaredOO:  # => OO solution: a strategy object with a single method
    def apply(self, nums: list[int]) -> list[int]:  # => the strategy's one method -- swappable via polymorphism
        return [n * n for n in nums if n % 2 == 0]  # => same computation, wrapped in an object identity


def _append_if_even_squared(acc: tuple[int, ...], n: int) -> tuple[int, ...]:  # => the fold's step function, fully typed so reduce() infers cleanly
    return acc + (n * n,) if n % 2 == 0 else acc  # => same rule as the other three solutions, expressed as a fold step


def evens_squared_functional(nums: tuple[int, ...]) -> tuple[int, ...]:  # => functional: a pure fold
    return reduce(_append_if_even_squared, nums, ())  # => no mutation, one fold expression


def evens_squared_declarative(nums: list[int]) -> list[int]:  # => declarative: states WHAT, one expression
    return [n * n for n in nums if n % 2 == 0]  # => a comprehension: reads as "the squares of the evens"


@dataclass(frozen=True)  # => one row of the portfolio's comparison matrix
class MatrixRow:  # => frozen=True -- a recorded comparison fact, never edited in place
    paradigm: str  # => which of the four solutions this row describes
    solution_ref: str  # => the concrete function/method name implementing it
    testable_in_isolation: bool  # => the one criterion this portfolio actually assesses


MATRIX: list[MatrixRow] = [  # => the comparison matrix: every solution above, with ONE criterion assessed
    MatrixRow("imperative", "evens_squared_imperative", testable_in_isolation=True),  # => row 1
    MatrixRow("oo", "EvensSquaredOO.apply", testable_in_isolation=True),  # => row 2
    MatrixRow("functional", "evens_squared_functional", testable_in_isolation=True),  # => row 3
    MatrixRow("declarative", "evens_squared_declarative", testable_in_isolation=True),  # => row 4
]  # => closes the matrix -- one row per solution, all independently testable

sample = [1, 2, 3, 4, 5, 6]  # => shared input, run through all four solutions
results = {  # => run every solution against the SAME input, to prove they agree
    "imperative": evens_squared_imperative(sample),  # => run solution 1
    "oo": EvensSquaredOO().apply(sample),  # => run solution 2
    "functional": list(evens_squared_functional(tuple(sample))),  # => run solution 3
    "declarative": evens_squared_declarative(sample),  # => run solution 4
}  # => closes the results dict -- one entry per paradigm, ready to compare
print(all(v == [4, 16, 36] for v in results.values()))  # => the matrix is only meaningful if all four agree
# => Output: True
print(len(MATRIX) == len(results))  # => the matrix covers EVERY solution present, none missing
# => Output: True
