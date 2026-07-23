"""Example 59: Four Paradigms, One Shared Test."""

from abc import ABC, abstractmethod  # => ABC/abstractmethod define way #2's strategy interface
from collections.abc import Callable  # => types the count_fn parameter shared_test() accepts below
from functools import reduce  # => reduce() is way #3's fold, threading a count through the list

TASK = "count how many numbers in a list are prime"  # => the ONE problem, solved four ways below


def is_prime(n: int) -> bool:  # => shared helper -- not itself part of the "four ways" comparison
    if n < 2:  # => 0, 1, and negatives are never prime by definition
        return False  # => reject immediately -- no need to try any divisor
    return all(n % d != 0 for d in range(2, int(n**0.5) + 1))  # => trial division up to sqrt(n)


def count_primes_imperative(nums: list[int]) -> int:  # => way #1: explicit loop + counter
    count = 0  # => mutable accumulator, starts at zero
    for n in nums:  # => explicit iteration over every candidate number
        if is_prime(n):  # => explicit selection: only count numbers that pass the shared check
            count += 1  # => explicit mutation: increment the running total
    return count  # => the fully built accumulator


class PrimeCounter(ABC):  # => way #2: OO -- an abstract strategy, one concrete implementation
    @abstractmethod  # => marks count() as required -- PrimeCounter itself can never be instantiated
    def count(self, nums: list[int]) -> int: ...  # => no body here -- only concrete subclasses implement it


class TrialDivisionPrimeCounter(PrimeCounter):  # => the concrete OO strategy
    def count(self, nums: list[int]) -> int:  # => satisfies the abstract count() contract above
        return sum(1 for n in nums if is_prime(n))  # => OO wraps the same core check in an object


def _count_or_skip(acc: int, n: int) -> int:  # => the fold's step function, fully typed so reduce() infers cleanly
    return acc + 1 if is_prime(n) else acc  # => same rule as the imperative/OO/declarative versions, expressed as a fold step


def count_primes_functional(nums: list[int]) -> int:  # => way #3: a pure fold, no mutation
    return reduce(_count_or_skip, nums, 0)  # => threads a count, no named accumulator


def count_primes_declarative(nums: list[int]) -> int:  # => way #4: states WHAT to count, not HOW
    return len([n for n in nums if is_prime(n)])  # => "the length of the list of primes"


def shared_test(count_fn: Callable[[list[int]], int]) -> bool:  # => the ONE test all four solutions must pass, given as a function
    sample = [2, 3, 4, 5, 6, 7, 8, 9, 10]  # => primes here: 2, 3, 5, 7 -- four of them
    return count_fn(sample) == 4  # => every paradigm's answer must equal 4


results = {  # => run all four paradigms against the SAME shared_test function
    "imperative": shared_test(count_primes_imperative),  # => way #1's verdict
    "oo": shared_test(TrialDivisionPrimeCounter().count),  # => way #2's verdict
    "functional": shared_test(count_primes_functional),  # => way #3's verdict
    "declarative": shared_test(count_primes_declarative),  # => way #4's verdict
}  # => closes the per-paradigm results table
print(results)  # => all four must pass the identical shared test
# => Output: {'imperative': True, 'oo': True, 'functional': True, 'declarative': True}
print(all(results.values()))  # => a single boolean summary
# => Output: True
