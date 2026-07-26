"""Example 2: pytest verification for Page Header Pack and Unpack."""

from example import HEADER_SIZE, pack_header, unpack_header


def test_header_size_is_four_bytes() -> None:
    assert HEADER_SIZE == 4  # => two uint16 fields pack into exactly 4 bytes


def test_pack_unpack_round_trips() -> None:
    packed = pack_header(100, 200)
    assert unpack_header(packed) == (
        100,
        200,
    )  # => unpack(pack(x)) always reproduces x exactly


def test_different_values_round_trip_independently() -> None:
    packed = pack_header(4, 4096)
    assert unpack_header(packed) == (
        4,
        4096,
    )  # => a second, independent pair round-trips too


# => Run: pytest -- Output: 3 passed
