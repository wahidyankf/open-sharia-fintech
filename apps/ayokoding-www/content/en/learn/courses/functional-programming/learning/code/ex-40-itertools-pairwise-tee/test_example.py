"""Example 40: pytest verification for Adjacent Pairs via pairwise and tee."""

from itertools import pairwise, tee


def test_pairwise_and_tee() -> None:
    readings = [1, 2, 4]
    assert list(pairwise(readings)) == [(1, 2), (2, 4)]

    stream_a, stream_b = tee(iter(readings))
    assert (
        next(stream_a) == next(stream_b) == 1
    )  # => independent streams, same starting point


# => Run: pytest -- Output: 1 passed
