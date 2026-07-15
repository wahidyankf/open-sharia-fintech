# learning/code/ex-18-mark-xfail/test_example.py
"""Example 18: Mark a Test xfail."""

import pytest  # => brings in @pytest.mark.xfail, another builtin marker (co-08)


def reverse_words(
    sentence: str,
) -> str:  # => the unit under test -- has a KNOWN bug below
    words = sentence.split(" ")  # => splits on a single space only
    return " ".join(words)  # => bug: this REJOINS in the SAME order -- it never reverses anything  # fmt: skip


def test_reverse_words_normal_case() -> (
    None
):  # => runs normally -- passes, included for contrast
    assert reverse_words("a b") != "a b b"  # => a trivially true assertion, unrelated to the known bug  # fmt: skip


@pytest.mark.xfail(reason="reverse_words has a known bug -- it never actually reverses")  # => co-08  # fmt: skip
def test_reverse_words_is_known_broken() -> None:
    # => this assertion is EXPECTED to fail, because of the real bug in reverse_words above
    assert reverse_words("hello world") == "world hello"  # => genuinely fails: bug returns "hello world"  # fmt: skip
    # => pytest reports this as "xfail" (expected failure), NOT as a suite-breaking "failed" --
    # => if this line ever started passing unexpectedly, pytest would instead report "XPASS"
