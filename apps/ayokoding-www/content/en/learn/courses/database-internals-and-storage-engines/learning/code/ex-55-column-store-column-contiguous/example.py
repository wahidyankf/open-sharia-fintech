"""Example 55: Column Store -- One Column's Values Are Byte-Adjacent."""
# A column store (co-28) lays out every ROW's value for ONE column contiguously, column by column.

import struct  # => stdlib fixed-width binary packing


def serialize_column_store(
    rows: list[tuple[int, int, float]],
) -> dict[str, bytes]:  # => one buffer PER column
    ids = bytearray()  # => the id column's own dedicated buffer
    quantities = bytearray()  # => the quantity column's own dedicated buffer
    prices = bytearray()  # => the price column's own dedicated buffer
    for (
        row_id,
        quantity,
        price,
    ) in rows:  # => walk rows once, but write each field to its OWN column buffer
        ids += struct.pack("i", row_id)  # => append to the id column ONLY
        quantities += struct.pack(
            "i", quantity
        )  # => append to the quantity column ONLY
        prices += struct.pack("f", price)  # => append to the price column ONLY
    return {
        "id": bytes(ids),
        "quantity": bytes(quantities),
        "price": bytes(prices),
    }  # => three separate columns


rows = [
    (1, 10, 9.99),
    (2, 20, 19.99),
]  # => the SAME two rows, three columns each, as ex-54
columns = serialize_column_store(rows)  # => the column-major byte layout
print(len(columns["price"]))  # => Output: 8

price0 = struct.unpack("f", columns["price"][0:4])[
    0
]  # => row 0's price, sliced from the price column ALONE
price1 = struct.unpack("f", columns["price"][4:8])[
    0
]  # => row 1's price, right next to row 0's in this buffer
print((round(price0, 2), round(price1, 2)))  # => Output: (9.99, 19.99)

assert (
    len(columns["price"]) == 8
)  # => two 4-byte floats, back-to-back, with NOTHING else interleaved
assert (
    len(columns) == 3
)  # => three independent column buffers -- one per field, not one per row
print("ex-55 OK")  # => Output: ex-55 OK
