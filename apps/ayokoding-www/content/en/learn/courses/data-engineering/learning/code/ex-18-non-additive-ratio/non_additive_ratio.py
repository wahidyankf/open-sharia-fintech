"""Worked Example 18: Non-Additive Ratio -- Store the Components, Divide at Query Time."""  # => co-10: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import duckdb  # => co-10: a non-additive ratio is checked by comparing averaging-the-ratio against ratio-of-sums

CONVERSION_ROWS = [  # => co-10: conversion RATE per campaign -- NON-additive -- never sum or average a rate directly
    ("campaign-A", 1000, 50),  # => co-10: 1000 visits, 50 conversions -- a 5% rate on a large sample
    ("campaign-B", 20, 10),  # => co-10: 20 visits, 10 conversions -- a 50% rate, but a TINY, skewed sample
    ("campaign-C", 500, 100),  # => co-10: 500 visits, 100 conversions -- a 20% rate on a medium sample
]  # => co-10: closes CONVERSION_ROWS -- (campaign, visits, conversions) -- campaign-B has a tiny denominator, a skewed rate

if __name__ == "__main__":  # => co-10: entry point -- runs only when this file executes directly, not on import
    con = duckdb.connect()  # => co-10: a fresh warehouse stand-in
    con.sql("CREATE TABLE fact_conversion (campaign VARCHAR, visits INTEGER, conversions INTEGER)")  # => co-10: store the COMPONENTS, not a precomputed rate
    con.executemany("INSERT INTO fact_conversion VALUES (?, ?, ?)", CONVERSION_ROWS)  # => co-10: land all three campaigns

    per_row_sql = "SELECT AVG(CAST(conversions AS DOUBLE) / visits) FROM fact_conversion"  # => co-10: WRONG -- average the per-row ratio, equally weighted
    per_row_rate = con.sql(per_row_sql).fetchone()[0]  # => co-10: averages (0.05, 0.50, 0.20) equally, letting campaign-B's tiny sample dominate
    ratio_sql = "SELECT SUM(conversions)::DOUBLE / SUM(visits) FROM fact_conversion"  # => co-10: RIGHT -- divide at query time, AFTER summing separately
    ratio_of_sums = con.sql(ratio_sql).fetchone()[0]  # => co-10: (50+10+100) / (1000+20+500) -- correctly weighted by actual visit volume
    print(f"Average of per-row ratios (WRONG): {per_row_rate:.4f}")  # => co-10: prints the misleading average
    print(f"Ratio of sums (RIGHT, divide at query time): {ratio_of_sums:.4f}")  # => co-10: prints the correctly-weighted rate

    they_differ = round(per_row_rate, 4) != round(ratio_of_sums, 4)  # => co-10: the claim ex-18 makes -- these two approaches disagree
    print(f"Averaging ratios differs from ratio-of-sums: {they_differ}")  # => co-10: prints the divergence check
    assert they_differ, "averaging a non-additive ratio must differ from computing the ratio of summed components"  # => co-10
    print(f"MATCH: {per_row_rate:.4f} (naive average) != {ratio_of_sums:.4f} (correct ratio-of-sums)")  # => co-10
    # => co-10: storing visits + conversions (not a precomputed rate) is what lets EVERY later query divide correctly
