"""Example 2: pytest verification for Initialize Fields in __init__."""

from example import Dog


def test_init_sets_name_field() -> None:
    assert (
        Dog("Rex").name == "Rex"
    )  # => __init__ stored the constructor argument on the instance


# => Run: pytest -- Output: 1 passed
