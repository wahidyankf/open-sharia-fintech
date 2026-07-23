"""Example 72: A Fully-Covered Function With Surviving Mutants -- Coverage Isn't Proof."""

from adult import is_adult


def test_is_adult_true() -> None:  # => co-21: THIS CALL alone already executes the function's  # fmt: skip
    # => only line -- coverage.py will mark it 100% covered from this ONE test onward
    assert is_adult(20) is True


def test_is_adult_false() -> None:  # => co-21: adds a SECOND call, but coverage was ALREADY 100%  # fmt: skip
    assert is_adult(10) is False
    # co-21 vs co-22: coverage.py only asks "did this line RUN" -- it never asks "was the
    # ASSERTION strong enough to notice if the line's LOGIC were subtly wrong." Both questions
    # matter, but they are genuinely DIFFERENT questions, which is the whole point of this example.
