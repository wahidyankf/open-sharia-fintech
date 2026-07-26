"""Example 58: pytest verification for Run-Length Encoding."""

from example import rle_decode, rle_encode


def test_rle_round_trips() -> None:
    column = ["x", "x", "y", "y", "y"]
    assert rle_decode(rle_encode(column)) == column


def test_rle_collapses_run_count_below_element_count() -> None:
    column = ["z"] * 20
    runs = rle_encode(column)
    assert len(runs) == 1
    assert runs[0] == ("z", 20)


# => Run: pytest -- Output: 2 passed
