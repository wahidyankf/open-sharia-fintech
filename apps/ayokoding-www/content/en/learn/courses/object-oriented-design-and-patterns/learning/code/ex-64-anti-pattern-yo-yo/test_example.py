"""Example 64: pytest verification that yo-yo inheritance is diagnosed and flattened."""

from example import LoyaltyPricer, count_hops_to_understand, flattened_discount


def test_yo_yo_hierarchy_requires_four_hops_to_understand_one_method() -> None:
    assert count_hops_to_understand(LoyaltyPricer, "discount") == 4  # => the smell, named as a number


def test_flattened_version_produces_the_identical_result() -> None:
    loyalty = LoyaltyPricer()
    original = round(loyalty.discount(100.0), 6)  # => the yo-yo version's result
    flattened = round(flattened_discount(100.0), 6)  # => the flattened version's result
    assert original == flattened  # => flattening changed nothing observable


def test_flattened_version_is_a_single_plain_function_with_no_hierarchy_at_all() -> None:
    assert flattened_discount.__module__ == "example"  # => defined once, at module level -- no MRO to walk at all
    assert not hasattr(flattened_discount, "__mro__")  # => a plain function has no inheritance chain to jump through


# => Run: pytest -q -- Output: 3 passed
