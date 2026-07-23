-- Example 32: Window Moving Average.
-- ROWS BETWEEN N PRECEDING AND CURRENT ROW (co-05) makes the frame EXPLICIT: a
-- sliding 3-day window, not the whole-history running total from Example 8.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS daily_sales CASCADE;

-- => resets state -- this example is fully self-contained
-- Same daily_sales shape as Example 8 -- one extra day (Jan 5) added so the
-- sliding window has room to visibly SLIDE past its first few rows.
CREATE TABLE daily_sales (
  sale_date DATE PRIMARY KEY,
-- Same NUMERIC(8, 2) precision convention as Example 8 -- exact decimal
-- arithmetic for the AVG computed inside each sliding window.
  amount NUMERIC(8, 2) NOT NULL
);

-- Values chosen so the moving average visibly changes shape as the window
-- fills up (day 1: 1 row) and then slides (day 4 onward: always exactly 3 rows).
INSERT INTO
  daily_sales (sale_date, amount)
VALUES
  ('2026-01-01', 100.00),
  ('2026-01-02', 50.00),
  ('2026-01-03', 75.00),
  ('2026-01-04', 120.00),
  ('2026-01-05', 90.00);

-- => 5 days -- the frame below only ever looks BACK at most 2 days
-- ROWS BETWEEN 2 PRECEDING AND CURRENT ROW (co-05) is an EXPLICIT frame: sum only
-- the current row plus the 2 rows immediately before it -- a sliding window, not
-- Example 8's ever-growing "everything since the start" default frame.
SELECT
  sale_date,
  amount,
-- ROUND wraps the window result exactly as in Example 9 -- a scalar function
-- applied AFTER the window function has already produced its per-row value.
  ROUND(
-- 2 PRECEDING AND CURRENT ROW is inclusive on both ends -- 3 rows total once
-- the window is fully "warmed up", which is why the label says 3day, not 2day.
    AVG(amount) OVER (
-- ROWS (not RANGE) is specified explicitly here because sale_date is UNIQUE per
-- row -- with a unique ORDER BY key the two frame modes agree, but writing ROWS
-- states the intent unambiguously (see Example 33 for when they diverge).
      ORDER BY
        sale_date ROWS BETWEEN 2 PRECEDING
        AND CURRENT ROW
    ),
    2
  ) AS moving_avg_3day
FROM
-- Early rows (Jan 1, Jan 2) have FEWER than 2 preceding rows available --
-- Postgres simply uses however many actually exist rather than padding with
-- NULLs or erroring, which is why Jan 1's average is just itself.
  daily_sales
-- The outer ORDER BY (again) only controls display order -- the window's own
-- ORDER BY sale_date already fixed which rows fall inside each 3-day frame.
ORDER BY
  sale_date;

-- => Jan 1: avg of just itself = 100.00 (only 1 row exists so far)
-- => Jan 3: avg of (100+50+75)/3 = 75.00 (full 3-row window)
-- => Jan 5: avg of (75+120+90)/3 = 95.00 (window has SLID forward)
-- Unlike Example 8's running total, this average never simply grows -- it can
-- rise or fall as new days enter the 3-day window and old ones age out of it,
-- which is the entire point of a MOVING average versus a cumulative one.
