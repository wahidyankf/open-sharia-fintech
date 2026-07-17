"""Example 49: pytest verification for Chaining Option-Returning Lookups."""

from example import Nothing, Some, find_user_then_city


def test_chain_short_circuits_on_the_first_miss() -> None:
    users = {"ana": "jakarta"}
    cities = {"jakarta": "Jakarta, Indonesia"}

    assert find_user_then_city(users, cities, "ana") == Some("Jakarta, Indonesia")
    assert find_user_then_city(users, cities, "budi") == Nothing()


# => Run: pytest -- Output: 1 passed
