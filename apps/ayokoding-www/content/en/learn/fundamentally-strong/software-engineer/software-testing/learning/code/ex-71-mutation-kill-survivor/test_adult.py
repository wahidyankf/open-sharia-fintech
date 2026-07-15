"""Example 71: Add a Test to Kill a Surviving Mutant -- Watch the Mutation Score Improve."""

from adult import is_adult


def test_is_adult_true() -> None:  # => Example 70's ORIGINAL two tests, unchanged  # fmt: skip
    assert is_adult(20) is True  # => still passes -- unchanged from Example 70  # fmt: skip


def test_is_adult_false() -> None:  # => Example 70's second original test, unchanged  # fmt: skip
    assert is_adult(10) is False  # => still passes -- unchanged from Example 70  # fmt: skip


def test_is_adult_boundary() -> None:  # => co-22/co-27: the NEW test, aimed straight at the gap  # fmt: skip
    # age=18 is the EXACT boundary `age >= 18` decides -- neither of the two tests above ever
    # exercised it, which is exactly why Example 70's `age > 18` and `age >= 19` mutants survived.
    assert is_adult(18) is True  # => `age > 18` on 18 is False (wrong) -- THIS kills that mutant  # fmt: skip
    # => `age >= 19` on 18 is also False (wrong) -- THIS SAME assertion kills that mutant too
