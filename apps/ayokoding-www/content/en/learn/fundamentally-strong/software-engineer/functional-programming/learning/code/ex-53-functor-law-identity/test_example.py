"""Example 53: pytest verification for The Functor Identity Law by Example."""

from example import Box, identity


def test_mapping_identity_changes_nothing_but_the_wrapper() -> None:
    original = Box(7)
    assert original.map(identity) == original  # => the functor identity law


# => Run: pytest -- Output: 1 passed
