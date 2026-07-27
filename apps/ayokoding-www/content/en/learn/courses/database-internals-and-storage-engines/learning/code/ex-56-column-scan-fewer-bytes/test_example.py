"""Example 56: pytest verification for Column Scan Byte Savings."""

from example import column_store_scan_bytes, row_store_scan_bytes


def test_column_store_reads_fewer_bytes_for_a_single_column_scan() -> None:
    rows = row_store_scan_bytes(500)
    cols = column_store_scan_bytes(500, column_width=4)
    assert cols < rows


def test_savings_scale_with_row_count() -> None:
    small = row_store_scan_bytes(10) - column_store_scan_bytes(10, column_width=4)
    large = row_store_scan_bytes(1000) - column_store_scan_bytes(1000, column_width=4)
    assert large > small


# => Run: pytest -- Output: 2 passed
