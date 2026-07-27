"""Example 54: pytest verification for Row Store Tuple Contiguity."""

from example import ROW_SIZE, serialize_row_store


def test_one_row_occupies_exactly_row_size_contiguous_bytes() -> None:
    data = serialize_row_store([(1, 1, 1.0)])
    assert len(data) == ROW_SIZE


def test_two_rows_are_laid_out_back_to_back() -> None:
    data = serialize_row_store([(1, 1, 1.0), (2, 2, 2.0)])
    assert len(data) == 2 * ROW_SIZE


# => Run: pytest -- Output: 2 passed
