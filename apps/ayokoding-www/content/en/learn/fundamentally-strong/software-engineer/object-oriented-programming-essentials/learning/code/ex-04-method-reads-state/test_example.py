"""Example 4: pytest verification for A Method That Reads Instance State."""

from example import Dog


def test_greet_contains_instance_name() -> None:
    d: Dog = Dog("Rex")
    assert "Rex" in d.greet()  # => the returned string embeds this instance's own name


# => Run: pytest -- Output: 1 passed
