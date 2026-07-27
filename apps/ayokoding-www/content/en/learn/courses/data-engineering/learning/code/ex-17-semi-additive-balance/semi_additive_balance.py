"""Worked Example 17: Semi-Additive Balance."""  # => co-10: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-10: a semi-additive fact is checked by comparing a valid non-time sum against an invalid time sum

BALANCE_ROWS = [  # => co-10: an account BALANCE -- SEMI-additive -- summable across accounts, NOT across time
    ("2026-07-01", "acct-A", 100.0),  # => co-10: acct-A, day 1
    ("2026-07-02", "acct-A", 120.0),  # => co-10: acct-A, day 2
    ("2026-07-03", "acct-A", 90.0),  # => co-10: acct-A, day 3
    ("2026-07-01", "acct-B", 200.0),  # => co-10: acct-B, day 1
    ("2026-07-02", "acct-B", 210.0),  # => co-10: acct-B, day 2
    ("2026-07-03", "acct-B", 205.0),  # => co-10: acct-B, day 3
]  # => co-10: closes BALANCE_ROWS -- two accounts, three days each -- balances are snapshots, not incremental deltas

if __name__ == "__main__":  # => co-10: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-10: a fresh warehouse stand-in
    con.sql("CREATE TABLE fact_balance (as_of_date DATE, account VARCHAR, balance DOUBLE)")  # => co-10: a snapshot fact -- one row per (account, date)
    con.executemany("INSERT INTO fact_balance VALUES (?, ?, ?)", BALANCE_ROWS)  # => co-10: land all six snapshot rows

    valid_sql = "SELECT SUM(balance) FROM fact_balance WHERE as_of_date = DATE '2026-07-03'"  # => co-10: VALID -- summing across the ACCOUNT dimension on a SINGLE date
    valid_sum_across_accounts = con.sql(valid_sql).fetchone()[0]  # => co-10: 90 + 205 -- both accounts' balance AS OF the same date, a meaningful total
    print(f"Valid: sum across accounts, on 2026-07-03: {valid_sum_across_accounts}")  # => co-10: prints the meaningful total

    naive_sql = "SELECT SUM(balance) FROM fact_balance WHERE account = 'acct-A'"  # => co-10: INVALID -- naively summing balance across ALL rows, mixing dates together
    naive_sum_across_time = con.sql(naive_sql).fetchone()[0]  # => co-10: 100+120+90 -- adds three SNAPSHOTS of the same account together, which means nothing
    last_known_sql = "SELECT balance FROM fact_balance WHERE account = 'acct-A' ORDER BY as_of_date DESC LIMIT 1"  # => co-10: the CORRECT way -- take the LATEST snapshot, never sum
    last_known_balance = con.sql(last_known_sql).fetchone()[0]  # => co-10: the account's actual current balance
    print(f"Naive (INVALID) sum across time for acct-A: {naive_sum_across_time} | Actual current balance: {last_known_balance}")  # => co-10

    time_sum_is_wrong = naive_sum_across_time != last_known_balance  # => co-10: the naive time-sum must NOT equal the real balance
    print(f"Time-summed value flagged as invalid (differs from actual balance): {time_sum_is_wrong}")  # => co-10
    assert valid_sum_across_accounts == 295.0, "summing across accounts, on one date, is a valid additive operation here"  # => co-10
    assert time_sum_is_wrong, "summing a balance across time must be flagged as invalid, unlike summing across accounts"  # => co-10
    print(f"MATCH: {valid_sum_across_accounts} (across accounts) is valid; {naive_sum_across_time} (across time) is not")  # => co-10
    # => co-10: semi-additive facts are additive across every dimension EXCEPT time -- summing across time silently lies
