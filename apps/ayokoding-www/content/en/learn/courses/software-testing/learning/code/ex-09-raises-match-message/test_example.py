# learning/code/ex-09-raises-match-message/test_example.py
"""Example 9: Raises with a Matching Message."""

import pytest  # => same pytest.raises context manager as ex-08, plus its match= parameter


def parse_positive_int(text: str) -> int:  # => identical unit under test to ex-08
    value = int(text)  # => ValueError here if text is not numeric at all
    if value <= 0:  # => the branch this example specifically targets
        raise ValueError(f"expected a positive integer, got {value}")  # => message MATTERS here  # fmt: skip
    return value  # => the success path, not exercised by this particular test


def test_raises_match_checks_the_message_text() -> None:
    # match= takes a regex, checked with re.search against str(exception) -- not equality
    with pytest.raises(ValueError, match="expected a positive integer, got -5"):  # => co-04  # fmt: skip
        parse_positive_int("-5")  # => act: raises ValueError("expected a positive integer, got -5")  # fmt: skip
    # => a DIFFERENT message (say, "bad input") would make this test fail even though a
    # => ValueError still fired -- match= asserts on THE EXCEPTION'S CONTENT, not just its type
