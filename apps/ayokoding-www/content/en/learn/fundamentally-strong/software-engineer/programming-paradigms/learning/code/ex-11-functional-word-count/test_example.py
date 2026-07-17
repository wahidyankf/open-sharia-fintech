"""Example 11: pytest verification for Functional Word Count."""

from example import tally_via_counter, tally_via_reduce


def test_both_functional_versions_match_the_imperative_counts() -> None:
    words: list[str] = str("the cat sat on the mat the cat ran").split()  # => identical sentence to ex-01
    expected = {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "ran": 1}
    assert dict(tally_via_counter(words)) == expected  # => Counter-based fold matches
    assert tally_via_reduce(words) == expected  # => reduce-based fold matches too


def test_neither_function_mutates_its_input_list() -> None:
    words = ["x", "y", "x"]  # => a small input we snapshot before calling
    before = list(words)  # => defensive copy for comparison
    tally_via_counter(words)  # => call #1, discard result -- only checking for side effects
    tally_via_reduce(words)  # => call #2, discard result -- only checking for side effects
    assert words == before  # => the caller's list is byte-identical to what it was before either call


# => Run: pytest -- Output: 2 passed
