"""Example 72: pytest verification for Minimum Window Substring."""

from example import min_window_substring


def test_classic_known_answer() -> None:
    assert min_window_substring("ADOBECODEBANC", "ABC") == "BANC"


def test_target_longer_than_source_is_impossible() -> None:
    assert min_window_substring("a", "aa") == ""


def test_result_always_contains_every_target_character() -> None:
    result = min_window_substring("aaflslflsldkalskaaa", "aaa")
    assert result.count("a") >= 3  # => must cover all three required 'a's


# => Run: pytest -- Output: 3 passed
