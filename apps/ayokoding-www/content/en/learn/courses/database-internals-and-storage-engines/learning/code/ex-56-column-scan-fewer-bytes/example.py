"""Example 56: A Column Scan Reads Fewer Bytes for a Single-Column Aggregate."""
# The row-vs-column trade-off (co-28), made concrete: bytes actually read for ONE column's aggregate.

import struct  # => stdlib fixed-width binary packing

ROW_FORMAT = (
    "iif"  # => id (4 bytes), quantity (4 bytes), price (4 bytes) -- 12 bytes per row
)
ROW_SIZE = struct.calcsize(
    ROW_FORMAT
)  # => the full width of one row, ALL columns included


def row_store_scan_bytes(
    row_count: int,
) -> int:  # => a row store MUST read every column to get any one
    return (
        row_count * ROW_SIZE
    )  # => no way to skip quantity/price bytes even if only price is wanted


def column_store_scan_bytes(
    row_count: int, column_width: int
) -> int:  # => reads ONLY the target column
    return row_count * column_width  # => id and quantity bytes are never touched at all


row_count = 1000  # => a modest table for this illustration
price_width = struct.calcsize("f")  # => 4 bytes -- the price column's own fixed width

row_bytes = row_store_scan_bytes(
    row_count
)  # => bytes a row store touches for a `SUM(price)`-style scan
column_bytes = column_store_scan_bytes(
    row_count, price_width
)  # => bytes a column store touches for the same
print(row_bytes)  # => Output: 12000
print(column_bytes)  # => Output: 4000

assert (
    column_bytes < row_bytes
)  # => the column store read fewer bytes for the SAME single-column aggregate
savings_ratio = (
    row_bytes / column_bytes
)  # => how many times more the row store had to read
print(round(savings_ratio, 2))  # => Output: 3.0
print("ex-56 OK")  # => Output: ex-56 OK
