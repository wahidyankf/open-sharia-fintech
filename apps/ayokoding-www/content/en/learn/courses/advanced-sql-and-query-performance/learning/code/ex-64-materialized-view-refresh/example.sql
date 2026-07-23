-- Example 64: Materialized View Refresh.
-- A materialized view (co-27) stores a query's RESULT physically on disk, like a
-- table -- fast to read, but it does NOT auto-update when the underlying data
-- changes. REFRESH MATERIALIZED VIEW recomputes it from scratch, on demand.
-- Suppress routine NOTICE messages so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

-- The materialized view must be dropped BEFORE its base table -- a materialized
-- view that references sale_row would otherwise block dropping sale_row underneath it.
DROP MATERIALIZED VIEW IF EXISTS daily_sales_summary CASCADE;

DROP TABLE IF EXISTS sale_row CASCADE;

-- => resets state -- this example is fully self-contained
-- price uses NUMERIC(10, 2), not FLOAT -- exact decimal arithmetic matters for
-- summed money totals, same reasoning as Example 1's book prices.
CREATE TABLE sale_row (
-- sale_date is a plain DATE, not TIMESTAMP -- GROUP BY sale_date below buckets
-- by calendar day, matching how a daily sales report is normally consumed.
  id INTEGER PRIMARY KEY,
  sale_date DATE NOT NULL,
  amount NUMERIC(10, 2) NOT NULL
);

-- Three rows split across two dates -- 2026-01-01 gets two sales (100 + 50 = 150),
-- 2026-01-02 gets one (200) -- a small but non-trivial GROUP BY result to summarize.
INSERT INTO
  sale_row (id, sale_date, amount)
VALUES
  (1, '2026-01-01', 100.00),
  (2, '2026-01-01', 50.00),
  (3, '2026-01-02', 200.00);

-- => 3 rows across 2 days -- the base data the view summarizes
-- A materialized view is defined with a query, exactly like a plain VIEW --
-- the difference is entirely in WHEN that query's results are computed.
CREATE MATERIALIZED VIEW daily_sales_summary AS
SELECT
  sale_date,
  -- SUM and COUNT are the two aggregates a materialized view most commonly
  -- precomputes -- both are expensive to recompute on every read against a
  -- large sale_row table, which is exactly the workload this pattern targets.
  SUM(amount) AS total_amount,
  COUNT(*) AS sale_count
FROM
  sale_row
GROUP BY
  sale_date;

-- => the aggregation runs ONCE, right now -- results are stored,
-- => NOT recomputed on every SELECT like a plain view would be
-- Reading FROM a materialized view is as fast as reading from an ordinary
-- table -- there is no aggregation cost paid at SELECT time, only at CREATE
-- or REFRESH time.
SELECT
  *
FROM
  daily_sales_summary
ORDER BY
  sale_date;

-- => reflects the data AS OF creation time
-- This new row lands in the SAME 2026-01-01 bucket the view already
-- summarized -- watch what the next SELECT shows before vs after REFRESH.
INSERT INTO
  sale_row (id, sale_date, amount)
VALUES
  (4, '2026-01-01', 999.00);

-- => a NEW sale is added to the base table
SELECT
  *
FROM
  daily_sales_summary
ORDER BY
  sale_date;

-- => STILL the OLD totals -- the materialized view has NOT
-- => noticed the new row at all -- this is the core tradeoff (co-27)
-- Nothing about INSERT, UPDATE, or DELETE on the base table EVER touches a
-- materialized view automatically -- an explicit REFRESH is always required.
-- REFRESH re-runs the ENTIRE defining query from scratch every time -- there
-- is no INCREMENTAL refresh in core PostgreSQL (unlike some other databases'
-- materialized views), so refresh cost scales with the full base-table size.
REFRESH MATERIALIZED VIEW daily_sales_summary;

-- => recomputes the ENTIRE view from scratch -- takes an
-- => ACCESS EXCLUSIVE lock, blocking concurrent reads while it runs
-- => (Example 75 covers the CONCURRENTLY variant that avoids this)
-- The plain (non-CONCURRENTLY) REFRESH used here is the simplest form -- fine
-- for batch/offline jobs, but risky for a view queried by live traffic.
SELECT
  *
FROM
  daily_sales_summary
ORDER BY
  sale_date;

-- => NOW reflects the new sale -- 2026-01-01's total jumped
-- The choice of WHEN to refresh (a cron job, a trigger, or CONCURRENTLY on a
-- schedule) is entirely an application decision -- PostgreSQL never refreshes
-- a materialized view on its own.
-- Combined with a scheduled job (cron, pg_cron, or an application worker),
-- REFRESH MATERIALIZED VIEW is the standard way to trade query-time freshness
-- for query-time speed on expensive aggregate reports.
