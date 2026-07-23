"""Example 74: pytest verification for A Deep pipe vs. Nested Calls on Real Data."""

from example import count_words, pipe, split_words, strip_whitespace, to_lowercase


def test_pipe_and_nested_calls_compute_the_identical_answer() -> None:
    raw = "  A  B  C  "
    nested = count_words(split_words(to_lowercase(strip_whitespace(raw))))
    piped = pipe(strip_whitespace, to_lowercase, split_words, count_words)(raw)
    assert nested == piped == 3


# => Run: pytest -- Output: 1 passed
