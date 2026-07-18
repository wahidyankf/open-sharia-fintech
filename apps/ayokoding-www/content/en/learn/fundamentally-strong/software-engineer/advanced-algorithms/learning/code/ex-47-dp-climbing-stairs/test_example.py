"""Example 47: pytest verification for Climbing Stairs DP."""

from example import count_ways_brute_force, count_ways_to_climb


def test_matches_brute_force_for_small_n() -> None:
    for n in range(15):
        assert count_ways_to_climb(n) == count_ways_brute_force(n)


def test_known_value_for_five_stairs() -> None:
    assert count_ways_to_climb(5) == 8


# => Run: pytest -- Output: 2 passed
