"""Example 63: A Lazy Prime Sieve Over an Infinite Generator."""

from itertools import (
    count,
    islice,
)  # => count: infinite lazy range; islice: pulls a bounded slice
from typing import Iterator  # => Iterator types both generators below


def natural_numbers_from(
    start: int,
) -> Iterator[int]:  # => an INFINITE generator -- never runs out
    yield from count(start)  # => delegates to itertools.count, lazily, forever


def sieve(
    numbers: Iterator[int],
) -> Iterator[int]:  # => a lazy, recursive Eratosthenes-style sieve
    first = next(
        numbers
    )  # => the next number is prime by construction (nothing smaller divided it)
    yield first  # => yields it immediately -- consumer can use it before the rest is computed
    yield from sieve(
        n for n in numbers if n % first != 0
    )  # => filters multiples, sieves the REST lazily


primes = sieve(
    natural_numbers_from(2)
)  # => an infinite lazy stream of primes -- nothing computed yet
first_ten = list(
    islice(primes, 10)
)  # => pulls EXACTLY 10 primes, the ONLY work this line forces

# => the classic functional demonstration that laziness makes infinite structures usable
print(first_ten)  # => Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
