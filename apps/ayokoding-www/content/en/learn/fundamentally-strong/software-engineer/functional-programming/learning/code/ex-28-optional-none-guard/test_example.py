"""Example 28: pytest verification for Guarding a None-Returning Function."""

from example import find_user_age


def test_hit_and_miss_are_both_handled() -> None:
    directory = {"ana": 30}
    assert find_user_age(directory, "ana") == 30
    assert find_user_age(directory, "citra") is None


# => Run: pytest -- Output: 1 passed
