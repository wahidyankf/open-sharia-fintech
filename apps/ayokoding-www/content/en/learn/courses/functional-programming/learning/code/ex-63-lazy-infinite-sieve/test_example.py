"""Example 63: pytest verification for A Lazy Prime Sieve Over an Infinite Generator."""

from itertools import islice

from example import natural_numbers_from, sieve


def test_sieve_produces_the_correct_first_primes() -> None:
    primes = sieve(natural_numbers_from(2))
    assert list(islice(primes, 5)) == [2, 3, 5, 7, 11]


# => Run: pytest -- Output: 1 passed
