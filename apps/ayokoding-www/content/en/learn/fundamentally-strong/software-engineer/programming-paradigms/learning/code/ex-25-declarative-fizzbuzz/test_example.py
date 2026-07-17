"""Example 25: pytest verification for Declarative FizzBuzz."""

from example import fizzbuzz_declarative, imperative_reference


def test_declarative_matches_the_known_imperative_result() -> None:
    assert fizzbuzz_declarative(20) == imperative_reference  # => byte-identical to example 24's output


def test_rule_priority_handles_fifteen_before_three_or_five() -> None:
    result = fizzbuzz_declarative(30)  # => wider range to also cover n=30
    assert result[14] == "FizzBuzz"  # => n=15: both divisors match, priority picks FizzBuzz first
    assert result[29] == "FizzBuzz"  # => n=30: same priority rule applies


# => Run: pytest -- Output: 2 passed
