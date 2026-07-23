-- Example 8: Window Running Total.
-- OVER() (co-04) computes a value ACROSS a set of rows without collapsing them into
-- groups -- unlike GROUP BY, every input row still appears once in the output.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS daily_sales CASCADE;

-- => resets state -- this example is fully self-contained
-- sale_date is used directly as the PRIMARY KEY (a natural key) rather than a
-- surrogate id -- appropriate here because "one row per calendar day" is a
-- real business invariant this table needs to enforce, not just a convenience.
CREATE TABLE daily_sales (
  sale_date DATE PRIMARY KEY,
-- NUMERIC(8, 2) allows totals up to 999999.99 -- sized generously above any
-- single day's amount so the running SUM across many days will not overflow.
  amount NUMERIC(8, 2) NOT NULL
);

-- => one row per day, currently empty
INSERT INTO
  daily_sales (sale_date, amount)
VALUES
  ('2026-01-01', 100.00),
  ('2026-01-02', 50.00),
  ('2026-01-03', 75.00),
  ('2026-01-04', 120.00);

-- => 4 days of sales; running total should reach 345.00
-- SUM(amount) OVER (ORDER BY sale_date) (co-04) is a running total: for each row,
-- it sums every row FROM THE START up to and including the current row's position.
SELECT
  sale_date,
  amount,
-- Because ORDER BY sale_date appears inside OVER() with no explicit frame clause,
-- Postgres defaults to "RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW" --
-- exactly the running-total behavior shown here. Example 33 shows how ties in
-- the ORDER BY column change this default's behavior, and how ROWS differs from
-- RANGE once duplicate ordering values are involved.
  SUM(amount) OVER (
    ORDER BY
      sale_date
  ) AS running_total
FROM
  daily_sales
-- This ORDER BY controls the DISPLAY order of the final result set -- it is a
-- separate concept from the ORDER BY inside OVER(), which controls the order
-- rows are CONSUMED when computing the running total. They happen to match
-- here, but window ORDER BY and outer ORDER BY are independent clauses.
ORDER BY
  sale_date;

-- => row 1: running_total 100.00 (itself only)
-- => row 4: running_total 345.00 (all 4 days summed)
-- A running total is only guaranteed non-decreasing when every summed value is
-- non-negative -- a table that also recorded refunds (negative amounts) would
-- produce a running_total that can drop between rows, which is still correct,
-- just less visually intuitive than this all-positive example.
