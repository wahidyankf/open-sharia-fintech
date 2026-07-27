"""Example 55: pytest verification for Column Store Column Contiguity."""

from example import serialize_column_store


def test_price_column_holds_only_price_bytes() -> None:
    columns = serialize_column_store([(1, 1, 1.5), (2, 2, 2.5)])
    assert len(columns["price"]) == 8  # => two 4-byte floats, nothing else


def test_three_columns_are_kept_in_three_separate_buffers() -> None:
    columns = serialize_column_store([(1, 1, 1.0)])
    assert set(columns.keys()) == {"id", "quantity", "price"}


# => Run: pytest -- Output: 2 passed
