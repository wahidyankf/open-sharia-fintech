# pyright: strict
"""Example 12: Offset Pagination's Cost -- fetch-and-discard. (co-04)

OFFSET makes the database "fetch and discard" every preceding row: to serve
offset=1000 it must walk past 1000 rows before returning the requested 10.
This example instruments a simulated query with a row-touch counter and shows
the touch count grows linearly with the offset. Source: "Use The Index, Luke
-- No Offset" (Markus Winand).
"""

ROWS_TOUCHED = [0]  # => a mutable counter cell -- how many rows the "query" scanned


def fetch_with_offset(offset: int, limit: int, table: list[int]) -> list[int]:
    ROWS_TOUCHED[0] = 0  # => reset the counter for this query
    page: list[int] = []  # => the rows actually returned
    for index, row in enumerate(table):  # => simulate the DB scanning the table in order
        ROWS_TOUCHED[0] += 1  # => EVERY row the scan passes is "touched", even skipped ones
        if index < offset:  # => co-04: rows before the offset are FETCHED then DISCARDED
            continue  # => touched but not returned -- this is the cost
        page.append(row)  # => a row that is BOTH touched AND returned
        if len(page) >= limit:  # => the page is full
            break  # => stop scanning immediately -- no extra row touched
    return page


TABLE = list(range(1, 10001))  # => 10000 rows -- a large enough table to make the cost visible

shallow = fetch_with_offset(offset=0, limit=10, table=TABLE)  # => page 1: touches only 10 rows
print(f"offset=0, limit=10    -> returned {len(shallow)} rows, touched {ROWS_TOUCHED[0]} rows")  # => Output: 10 touched

deep = fetch_with_offset(offset=1000, limit=10, table=TABLE)  # => page ~101: touches 1010 rows
print(f"offset=1000, limit=10 -> returned {len(deep)} rows, touched {ROWS_TOUCHED[0]} rows")  # => Output: 1010 touched

deeper = fetch_with_offset(offset=5000, limit=10, table=TABLE)  # => a deep page: touches 5010 rows
print(f"offset=5000, limit=10 -> returned {len(deeper)} rows, touched {ROWS_TOUCHED[0]} rows")  # => Output: 5010 touched

# The returned COUNT is always 10, but the touched count grows linearly with offset -- the fetch-and-discard cost.
assert len(shallow) == len(deep) == len(deeper) == 10  # => same page size
assert ROWS_TOUCHED[0] == 5010  # => the deep page paid for 5010 touches to return 10 rows
