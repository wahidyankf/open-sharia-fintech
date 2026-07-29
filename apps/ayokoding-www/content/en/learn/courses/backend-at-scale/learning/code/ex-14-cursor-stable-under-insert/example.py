# pyright: strict
"""Example 14: Cursor Stability Under Concurrent Insert. (co-05)

Because a cursor anchors to a position IN THE DATA (the last-seen id), it is
unaffected by a row inserted BEFORE the next page. An equivalent OFFSET page
DRIFTS: a new row near the front shifts every later position, so the offset
page either skips or repeats a row. Source: "Use The Index, Luke -- No Offset".
"""

ROWS = list(range(1, 11))  # => 10 rows, ids 1..10 (mutated below by a mid-scan insert)


def page_cursor(rows: list[int], starting_after: int | None, limit: int) -> list[int]:
    threshold = 0 if starting_after is None else starting_after  # => resume point IN the data
    return [r for r in rows if r > threshold][:limit]  # => co-05: WHERE id > cursor, stable under inserts


def page_offset(rows: list[int], offset: int, limit: int) -> list[int]:
    return rows[offset : offset + limit]  # => co-04: raw position -- drifts if rows shift


# Take the first page (ids 1..3), establishing a cursor/offset at id 3.
first_cursor = page_cursor(ROWS, None, 3)  # => [1, 2, 3]
first_offset = page_offset(ROWS, 0, 3)  # => [1, 2, 3]
print(f"page 1 (cursor): {first_cursor}")  # => Output: [1, 2, 3]
print(f"page 1 (offset): {first_offset}")  # => Output: [1, 2, 3]

# A new row is inserted at the FRONT of the list mid-scan (simulating a concurrent insert).
ROWS.insert(0, 0)  # => now [0, 1, 2, ..., 10] -- a row landed near the front

next_cursor = page_cursor(ROWS, starting_after=3, limit=3)  # => co-05: WHERE id > 3 -> [4, 5, 6] (unaffected)
next_offset = page_offset(ROWS, offset=3, limit=3)  # => co-04: position 3 shifted -> [3, 4, 5] (REPEATS id 3)
print(f"page 2 (cursor), after insert: {next_cursor}")  # => Output: [4, 5, 6] -- stable, no repeat
print(f"page 2 (offset), after insert: {next_offset}")  # => Output: [3, 4, 5] -- DRIFTED, id 3 repeated

assert next_cursor == [4, 5, 6]  # => co-05: cursor page is unaffected by the insert
assert 3 in next_offset and 3 not in next_cursor  # => co-04: offset page repeated id 3; cursor did not
