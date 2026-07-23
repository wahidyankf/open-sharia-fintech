"""Example 5: pytest verification for Goto-Free Loop."""

from example import first_over_ten_clean, first_over_ten_hacky


def test_both_versions_agree_on_a_hit() -> None:
    sample = [3, 7, 2, 15, 9, 20]  # => contains a value over 10
    assert first_over_ten_hacky(sample) == first_over_ten_clean(sample) == 15


def test_both_versions_agree_on_a_miss() -> None:
    sample = [1, 2, 3]  # => no value over 10 anywhere
    assert first_over_ten_hacky(sample) is None  # => hacky version returns None on a miss
    assert first_over_ten_clean(sample) is None  # => clean version must also return None


# => Run: pytest -- Output: 2 passed
