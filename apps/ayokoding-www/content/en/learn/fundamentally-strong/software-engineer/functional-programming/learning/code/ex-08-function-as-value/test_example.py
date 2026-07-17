"""Example 8: pytest verification for A Function Assigned to a Variable."""

from example import shout


def test_alias_behaves_identically() -> None:
    greeter = shout  # => same function object, new name
    assert greeter is shout  # => not a copy
    assert greeter("hi") == shout("hi") == "HI!"


# => Run: pytest -- Output: 1 passed
