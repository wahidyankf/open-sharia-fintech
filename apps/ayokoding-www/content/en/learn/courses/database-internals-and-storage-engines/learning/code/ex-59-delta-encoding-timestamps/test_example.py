"""Example 59: pytest verification for Delta Encoding of Monotonic Timestamps."""

from example import delta_decode, delta_encode


def test_delta_encoding_round_trips() -> None:
    timestamps = [100, 105, 111, 120]
    base, deltas = delta_encode(timestamps)
    assert delta_decode(base, deltas) == timestamps


def test_deltas_are_small_relative_to_the_full_values() -> None:
    timestamps = [1000000, 1000002, 1000005]
    _, deltas = delta_encode(timestamps)
    assert all(delta < 10 for delta in deltas)


# => Run: pytest -- Output: 2 passed
