"""Worked Example 36: Data Quality -- Validity (Range Check)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-16: a validity check is an ordinary COUNT ... WHERE column NOT BETWEEN query

if __name__ == "__main__":  # => co-16: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-16: a fresh warehouse stand-in
    con.sql("CREATE TABLE ratings (review_id INTEGER, stars INTEGER)")  # => co-16: stars must be within [1, 5] -- VALIDITY is the dimension under test
    con.executemany("INSERT INTO ratings VALUES (?, ?)", [(1, 5), (2, 3), (3, 9), (4, 1)])  # => co-16: review 3's stars=9 is out of the valid [1,5] range

    out_of_range = con.sql(  # => co-16: the validity check itself -- which rows fall outside the declared valid range?
        "SELECT review_id, stars FROM ratings WHERE stars NOT BETWEEN 1 AND 5"  # => co-16: stars outside [1,5] is the out-of-range condition being tested
    ).df()  # => co-16: every row that violates the [1,5] validity constraint
    validity_passed = len(out_of_range) == 0  # => co-16: the batch passes ONLY if every value is within its declared valid range
    print(f"Out-of-range rows:\n{out_of_range}\nValidity check passed: {validity_passed}")  # => co-16
    assert not validity_passed, "a batch with an out-of-range value must fail the validity check"  # => co-16: the claim ex-36 makes
    assert out_of_range["review_id"].tolist() == [3], "the check must identify exactly review_id 3 as out of range"  # => co-16

    con.sql("DELETE FROM ratings WHERE stars NOT BETWEEN 1 AND 5")  # => co-16: fix the batch -- remove the invalid row
    out_of_range_after_fix = con.sql("SELECT COUNT(*) FROM ratings WHERE stars NOT BETWEEN 1 AND 5").fetchone()[0]  # => co-16: re-run the SAME check
    print(f"Out-of-range rows after fix: {out_of_range_after_fix}")  # => co-16: prints the post-fix check
    assert out_of_range_after_fix == 0, "the same check must pass once the out-of-range row is removed"  # => co-16
    print("MATCH: the validity check correctly fails a batch with an out-of-range value, and passes once fixed")  # => co-16
    # => co-16: validity catches a value that IS present and typed correctly, but is still nonsensical for its declared domain
