"""Example 2: pytest verification for Procedural Decompose."""

from example import main, tally, tokenize


def test_output_identical_to_example_one() -> None:
    result: dict[str, int] = main("the cat sat on the mat the cat ran")  # => same sentence as ex-01
    assert result == {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1, "ran": 1}
    # => byte-identical result dict to the inline imperative version


def test_procedures_are_independently_callable() -> None:
    # => procedural abstraction means each named piece works stand-alone, not just glued in main()
    words = tokenize("a a b")  # => call tokenize() in isolation
    assert words == ["a", "a", "b"]  # => tokenize does exactly one job
    assert tally(words) == {"a": 2, "b": 1}  # => tally does exactly one job, given any word list


# => Run: pytest -- Output: 2 passed
