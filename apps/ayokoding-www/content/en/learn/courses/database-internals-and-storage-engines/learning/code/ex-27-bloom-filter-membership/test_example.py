"""Example 27: pytest verification for Bloom Filter Membership."""

from example import HASH_COUNT, add, bit_positions, might_contain


def test_added_key_is_reported_present() -> None:
    add("carol")
    assert might_contain("carol") is True


def test_bit_positions_returns_hash_count_positions() -> None:
    positions = bit_positions("dave")
    assert (
        len(positions) == HASH_COUNT
    )  # => one candidate bit per independent hash function


# => Run: pytest -- Output: 2 passed
