"""Example 24: pytest verification for Imperative FizzBuzz."""

from example import fizzbuzz_imperative


def test_1_to_20_matches_the_classic_sequence() -> None:
    result = fizzbuzz_imperative(20)  # => same range as the module-level demo
    assert result[:5] == ["1", "2", "Fizz", "4", "Buzz"]  # => the first five entries
    assert result[14] == "FizzBuzz"  # => index 14 is n=15, divisible by both 3 and 5
    assert len(result) == 20  # => exactly twenty entries produced


def test_multiples_of_fifteen_say_fizzbuzz_not_fizz_or_buzz() -> None:
    result = fizzbuzz_imperative(30)  # => a wider range to catch n=30 too
    assert result[29] == "FizzBuzz"  # => index 29 is n=30
    assert "Fizz" not in [result[14]]  # => n=15 must say FizzBuzz, never just Fizz


# => Run: pytest -- Output: 2 passed
