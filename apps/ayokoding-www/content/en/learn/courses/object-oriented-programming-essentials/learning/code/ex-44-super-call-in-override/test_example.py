"""Example 44: pytest verification for Calling super() Inside an Override."""

from example import Cat


def test_override_combines_base_and_subclass_output() -> None:
    result: str = Cat().speak()
    assert "Meow" in result  # => the subclass's own contribution
    assert "..." in result  # => the base implementation's contribution, via super()


# => Run: pytest -- Output: 1 passed
