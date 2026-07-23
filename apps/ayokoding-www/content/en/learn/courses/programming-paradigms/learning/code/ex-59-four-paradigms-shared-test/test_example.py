"""Example 59: pytest verification for Four Paradigms, One Shared Test."""

from example import (
    TrialDivisionPrimeCounter,
    count_primes_declarative,
    count_primes_functional,
    count_primes_imperative,
    shared_test,
)


def test_all_four_paradigm_implementations_pass_the_shared_test() -> None:
    assert shared_test(count_primes_imperative)  # => way #1
    assert shared_test(TrialDivisionPrimeCounter().count)  # => way #2
    assert shared_test(count_primes_functional)  # => way #3
    assert shared_test(count_primes_declarative)  # => way #4


def test_all_four_agree_on_a_second_independent_sample() -> None:
    sample = [11, 12, 13, 14, 15, 16, 17]  # => primes here: 11, 13, 17 -- three of them
    counts = {
        count_primes_imperative(sample),
        TrialDivisionPrimeCounter().count(sample),
        count_primes_functional(sample),
        count_primes_declarative(sample),
    }
    assert counts == {3}  # => a set of size 1 proves all four returned the SAME value


# => Run: pytest -- Output: 2 passed
