"""Example 28: pytest verification for Bloom Filter No False Negatives."""

from example import add, might_contain


def test_every_added_key_is_found_even_at_scale() -> None:
    keys = [f"item-{i}" for i in range(50)]
    for key in keys:
        add(key)
    assert all(
        might_contain(key) for key in keys
    )  # => zero false negatives across 50 fresh keys


def test_a_freshly_added_key_is_immediately_findable() -> None:
    add("just-added")
    assert might_contain("just-added") is True


# => Run: pytest -- Output: 2 passed
