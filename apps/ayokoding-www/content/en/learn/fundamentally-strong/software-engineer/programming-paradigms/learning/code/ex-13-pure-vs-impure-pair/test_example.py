"""Example 13: pytest verification for Pure vs Impure Pair."""

import example
from example import normalize, normalize_and_log


def test_pure_function_is_referentially_transparent() -> None:
    before = list(example.log)  # => snapshot the side-channel before calling the pure function
    a = normalize("  Foo Bar  ")  # => call #1
    b = normalize("  Foo Bar  ")  # => call #2, identical argument
    assert a == b == "foo bar"  # => same input always yields the same output
    assert example.log == before  # => the pure function left the side channel completely untouched


def test_impure_twin_computes_the_same_value_but_also_logs() -> None:
    before_len = len(example.log)  # => how many log entries exist before this call
    result = normalize_and_log("  Foo Bar  ")  # => same computation as normalize(), plus a side effect
    assert result == "foo bar"  # => the return value matches the pure version
    assert len(example.log) == before_len + 1  # => exactly one new entry was appended


# => Run: pytest -- Output: 2 passed
