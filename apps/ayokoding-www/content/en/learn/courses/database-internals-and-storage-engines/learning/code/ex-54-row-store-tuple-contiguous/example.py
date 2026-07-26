"""Example 54: Row Store -- One Row's Fields Are Byte-Adjacent."""
# A row store (co-28) lays out every field of ONE row contiguously before the next row begins.

import struct  # => stdlib fixed-width binary packing

ROW_FORMAT = (
    "iif"  # => two 4-byte ints (id, quantity) and one 4-byte float (price), per row
)
ROW_SIZE = struct.calcsize(ROW_FORMAT)  # => the exact byte width of one packed row


def serialize_row_store(
    rows: list[tuple[int, int, float]],
) -> bytes:  # => co-28: tuple-by-tuple layout
    buf = (
        bytearray()
    )  # => the growing byte buffer -- one row's worth appended at a time
    for (
        row_id,
        quantity,
        price,
    ) in rows:  # => walk rows in order, writing each one fully before the next
        buf += struct.pack(
            ROW_FORMAT, row_id, quantity, price
        )  # => id, quantity, price -- ALL adjacent
    return bytes(buf)  # => the final, immutable row-store byte layout


rows = [(1, 10, 9.99), (2, 20, 19.99)]  # => two rows, three columns each
data = serialize_row_store(rows)  # => the row-major byte layout
print(len(data))  # => Output: 24

row0_start = 0 * ROW_SIZE  # => byte offset where row 0 begins
row0_bytes = data[
    row0_start : row0_start + ROW_SIZE
]  # => ALL of row 0's fields, one contiguous slice
row0_id, row0_qty, row0_price = struct.unpack(
    ROW_FORMAT, row0_bytes
)  # => unpack confirms it round-trips
print((row0_id, row0_qty, row0_price))  # => Output: (1, 10, 9.989999771118164)

assert row0_id == 1  # => the row we asked for came back correctly
assert (
    len(row0_bytes) == ROW_SIZE
)  # => one row's fields fit in exactly ROW_SIZE contiguous bytes
print("ex-54 OK")  # => Output: ex-54 OK
