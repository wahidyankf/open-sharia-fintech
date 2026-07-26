"""Worked Example 10: Incremental Filter by Watermark."""  # => co-06: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-06: the incremental filter is expressed as an ordinary SQL WHERE clause

SOURCE_ROWS = [  # => co-06: eight source rows, spanning several days -- only SOME are "new" relative to a watermark
    (8001, "2026-07-01"),  # => co-06: day 1 -- before the watermark
    (8002, "2026-07-02"),  # => co-06: day 2 -- before the watermark
    (8003, "2026-07-03"),  # => co-06: day 3 -- before the watermark
    (8004, "2026-07-04"),  # => co-06: day 4 -- before the watermark
    (8005, "2026-07-05"),  # => co-06: day 5 -- AT the watermark, not strictly after it
    (8006, "2026-07-06"),  # => co-06: day 6 -- after the watermark, NEW
    (8007, "2026-07-07"),  # => co-06: day 7 -- after the watermark, NEW
    (8008, "2026-07-08"),  # => co-06: day 8 -- after the watermark, NEW
]  # => co-06: closes SOURCE_ROWS -- eight rows, one per day, 2026-07-01 through 2026-07-08

LAST_WATERMARK = "2026-07-05"  # => co-06: "the last row this pipeline has already processed" -- everything up to and including this date

if __name__ == "__main__":  # => co-06: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-06: a fresh warehouse stand-in
    con.sql("CREATE TABLE source_events (event_id INTEGER, event_date DATE)")  # => co-06: the upstream source, unfiltered
    con.executemany("INSERT INTO source_events VALUES (?, ?)", SOURCE_ROWS)  # => co-06: land every source row

    new_rows = con.sql(f"SELECT * FROM source_events WHERE event_date > DATE '{LAST_WATERMARK}' ORDER BY event_id").df()  # => co-06: STRICTLY after the watermark
    print(f"Watermark: {LAST_WATERMARK} | New rows found: {len(new_rows)}")  # => co-06: prints the watermark and the count
    print(new_rows)  # => co-06: prints exactly the rows this incremental run will process

    expected_new_ids = {8006, 8007, 8008}  # => co-06: 2026-07-06, 07, 08 -- the three days strictly after the watermark
    actual_new_ids = set(new_rows["event_id"].tolist())  # => co-06: what the incremental filter actually selected
    print(f"Expected new ids: {sorted(expected_new_ids)} | Actual: {sorted(actual_new_ids)}")  # => co-06: prints both sets
    assert actual_new_ids == expected_new_ids, "the incremental filter must select only rows newer than the watermark"  # => co-06
    print(f"MATCH: only {len(new_rows)} of {len(SOURCE_ROWS)} source rows are newer than the watermark")  # => co-06
    # => co-06: processing only the delta since the watermark is what keeps a routine run cheap, day after day
