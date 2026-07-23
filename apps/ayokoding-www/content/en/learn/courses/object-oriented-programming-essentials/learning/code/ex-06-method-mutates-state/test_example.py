"""Example 6: pytest verification for A Method That Mutates Instance State."""

from example import Dog


def test_rename_mutates_name_in_place() -> None:
    d: Dog = Dog("Rex")
    d.rename("Max")  # => mutates the existing instance
    assert d.name == "Max"  # => the SAME object now reports the new name


# => Run: pytest -- Output: 1 passed
