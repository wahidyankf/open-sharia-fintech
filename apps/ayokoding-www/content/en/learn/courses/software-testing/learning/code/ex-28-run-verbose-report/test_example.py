# learning/code/ex-28-run-verbose-report/test_example.py
"""Example 28: A Verbose Test Report."""


# ex-28: three tests -- two pass, one fails -- run with -v to see each one named individually (co-27, co-02)  # fmt: skip
def is_palindrome(text: str) -> bool:  # => the unit under test
    return text == text[::-1]  # => reversed-string comparison -- simple, deliberately no normalization  # fmt: skip


def test_racecar_is_a_palindrome() -> None:  # => PASSES -- shown by name in -v output
    assert is_palindrome("racecar")  # => "racecar" reversed is still "racecar"


def test_hello_is_not_a_palindrome() -> (
    None
):  # => PASSES -- also shown by name in -v output
    assert not is_palindrome(
        "hello"
    )  # => "hello" reversed is "olleh" -- correctly not equal


def test_mixed_case_palindrome_without_normalization() -> None:  # => FAILS -- deliberately, to show -v's PASS/FAIL mix  # fmt: skip
    # => "Racecar" reversed is "racecaR" -- differs by case, since is_palindrome does
    # => no case-folding -- this test intentionally exposes that limitation
    assert is_palindrome(
        "Racecar"
    )  # => genuinely False -- this assert fails on purpose
