-- Example 11: Lag/Lead Delta.
-- LAG (co-06) reaches BACK to a previous row's value within the current row's
-- computation -- here, the previous month's revenue -- without a self-join.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS monthly_revenue CASCADE;

-- => resets state -- this example is fully self-contained
-- month, used as the PRIMARY KEY, is always the FIRST of its month (2026-01-01,
-- 2026-02-01, ...) -- a common convention for storing monthly-grain time series.
CREATE TABLE monthly_revenue (
  month DATE PRIMARY KEY,
-- NUMERIC(10, 2) leaves room for revenue values into the tens of millions --
-- comfortably above the four-figure monthly totals seeded below.
  revenue NUMERIC(10, 2) NOT NULL
);

-- => one row per month, currently empty
INSERT INTO
  monthly_revenue (month, revenue)
VALUES
  ('2026-01-01', 10000.00),
  ('2026-02-01', 12000.00),
  ('2026-03-01', 9000.00),
  ('2026-04-01', 15000.00);

-- => 4 months; the FIRST month has no prior month to compare
-- LAG(revenue, 1) OVER (ORDER BY month) (co-06) fetches the PRIOR row's revenue --
-- month 1 has none, so LAG returns NULL there (no default 3rd argument given).
SELECT
  month,
  revenue,
-- LAG's second argument (1) is the OFFSET -- how many rows back to reach; LAG
-- also accepts an optional third argument, a DEFAULT value to substitute instead
-- of NULL when the offset row does not exist (not used here, so NULL surfaces).
  LAG (revenue, 1) OVER (
    ORDER BY
      month
  ) AS prior_month_revenue,
-- The delta expression recomputes the SAME LAG(revenue, 1) OVER (...) a second
-- time rather than reusing prior_month_revenue -- window functions cannot be
-- referenced by their output alias within the same SELECT list; a repeated
-- window expression (or a wrapping subquery/CTE) is the only way around that.
  revenue - LAG (revenue, 1) OVER (
    ORDER BY
      month
  ) AS delta
FROM
-- NULL minus a number is NULL, not an error and not treated as zero -- that is
-- why January's delta is NULL rather than a large negative "missing baseline" value.
  monthly_revenue
-- ORDER BY month here (again) guarantees display order -- LAG's own OVER (ORDER
-- BY month) already fixed WHICH row counts as "prior"; a mismatched outer ORDER
-- BY would only reorder the display, not change which value LAG picked up.
ORDER BY
  month;

-- => Jan: prior_month_revenue NULL, delta NULL (nothing before it)
-- => Feb: prior 10000.00, delta +2000.00 (12000 - 10000)
-- => Mar: prior 12000.00, delta -3000.00 (revenue DROPPED)
-- LEAD() is LAG's mirror image -- it reaches FORWARD instead of back -- useful
-- for "days until next event" style calculations; this example sticks to LAG
-- to keep the running-delta narrative in one direction.
