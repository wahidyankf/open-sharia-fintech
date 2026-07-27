"""Example 47: pytest verification for Heap Secondary Index Pointers."""

from example import secondary_lookup


def test_secondary_lookup_resolves_through_the_pointer_to_the_heap_row() -> None:
    result = secondary_lookup("carol@example.com")
    assert result == "carol@example.com"


def test_missing_key_returns_none_without_touching_the_heap() -> None:
    result = secondary_lookup("nobody@example.com")
    assert result is None


# => Run: pytest -- Output: 2 passed
