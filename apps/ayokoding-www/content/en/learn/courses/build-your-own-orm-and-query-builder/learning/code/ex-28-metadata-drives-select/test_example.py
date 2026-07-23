"""Example 28: pytest verification for Metadata-Driven SELECT."""

from example import Column, TableMeta, select_all_columns


def test_column_order_matches_registration_order() -> None:
    # => columns registered in a deliberately unusual order (not alphabetical)
    meta = TableMeta(name="orders", columns=(Column(name="total"), Column(name="id"), Column(name="status")))
    sql = select_all_columns(meta)  # => must preserve that exact order
    assert sql == "SELECT total, id, status FROM orders"  # => registration order, not alphabetical


def test_single_column_table() -> None:
    meta = TableMeta(name="flags", columns=(Column(name="enabled"),))  # => a one-column edge case
    assert select_all_columns(meta) == "SELECT enabled FROM flags"  # => no trailing comma, no join artifact


# => Run: pytest -- Output: 2 passed
