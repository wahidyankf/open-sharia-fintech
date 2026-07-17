"""Example 80: pytest verification for A Functional-Core Log Analyzer With Result Errors and an Applicative Combine."""

from example import Err, Ok, count_by_level, parse_all


def test_core_accumulates_every_malformed_line_and_counts_the_rest() -> None:
    good = ["INFO:a", "WARN:b", "INFO:c"]
    result = parse_all(good)
    assert isinstance(result, Ok)
    assert count_by_level(result.value) == {"INFO": 2, "WARN": 1}

    bad = ["INFO:a", "nonsense", "also nonsense"]
    bad_result = parse_all(bad)
    assert isinstance(bad_result, Err)
    assert (
        len(bad_result.errors) == 2
    )  # => BOTH malformed lines reported, not just the first


# => Run: pytest -- Output: 1 passed
