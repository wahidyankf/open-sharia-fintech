-- Example 68: LATERAL Cross-Apply Report.
-- A LATERAL join (co-09) can power a multi-column dashboard query in ONE query:
-- for each customer, pull their most recent order AND their lifetime order count
-- via two separate LATERAL subqueries -- correlated, but each returns its own shape.
-- Suppress routine NOTICE messages so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

-- Both tables are dropped together -- customer_order references dash_customer,
-- so listing them in one DROP avoids a FK-ordering headache on repeated runs.
DROP TABLE IF EXISTS customer_order,
dash_customer CASCADE;

-- => resets state -- this example is fully self-contained
-- dash_customer is deliberately tiny (3 rows) -- the interesting part of this
-- example is the LATERAL query SHAPE, not a large dataset.
CREATE TABLE dash_customer (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- order_date is a plain DATE, and amount uses NUMERIC(10,2) for exact money
-- math, matching the convention used throughout this topic.
CREATE TABLE customer_order (
  -- id is a simple surrogate key -- customer_id in customer_order below
  -- references this column implicitly (no explicit FK for brevity here).
  id INTEGER PRIMARY KEY,
  -- customer_id has no FK constraint here for brevity -- production schemas
  -- would typically add REFERENCES dash_customer(id) on this column.
  customer_id INTEGER NOT NULL,
  order_date DATE NOT NULL,
  -- amount uses NUMERIC(10,2), the same money-precision convention used
  -- consistently across every example in this topic.
  amount NUMERIC(10, 2) NOT NULL
);

INSERT INTO
  dash_customer (id, name)
VALUES
  -- Three customers, seeded before customer_order so the LATERAL queries
  -- below always find a matching customer_id for every order row.
  (1, 'Alice'),
  (2, 'Bob'),
  (3, 'Cara');

-- Alice gets 3 orders, Bob 1, Cara 2 -- an uneven distribution so the
-- lifetime_order_count column below shows genuinely different numbers per row.
INSERT INTO
  customer_order (id, customer_id, order_date, amount)
VALUES
  -- Alice's three orders span three months -- 2026-03-01 is the LATEST,
  -- confirming which row LATERAL #1's ORDER BY DESC LIMIT 1 should surface.
  (1, 1, '2026-01-01', 50.00),
  (2, 1, '2026-02-01', 75.00),
  (3, 1, '2026-03-01', 30.00),
  (4, 2, '2026-01-15', 200.00),
  (5, 3, '2026-01-01', 10.00),
  (6, 3, '2026-01-10', 20.00);

-- => Alice: 3 orders, Bob: 1 order, Cara: 2 orders
-- This index is what makes LATERAL #1's ORDER BY order_date DESC LIMIT 1
-- efficient -- it can walk the index in already-sorted order per customer_id
-- instead of sorting each customer's orders from scratch.
CREATE INDEX idx_customer_order_customer_date ON customer_order (customer_id, order_date DESC);

-- ANALYZE refreshes the planner's row-count and distribution statistics --
-- without it, a freshly-populated table can fool the planner into a
-- suboptimal plan choice for the LATERAL subqueries below.
ANALYZE dash_customer;

-- Both tables are analyzed after seeding, not before -- statistics collected
-- on an empty table would not reflect the 3-customer, 6-order reality below.
ANALYZE customer_order;

-- Two independent LATERAL subqueries, each correlated to the SAME outer row
-- (c.id), let this single query answer two logically DIFFERENT questions per
-- customer without a separate round trip or a UNION of differently-shaped queries.
SELECT
  c.name,
  latest.order_date AS most_recent_order_date,
  latest.amount AS most_recent_order_amount,
  -- Both latest.* and stats.* columns come from DIFFERENT LATERAL
  -- subqueries but the SAME outer c.id -- the SELECT list simply projects
  -- whichever columns each LATERAL alias exposes.
  stats.order_count AS lifetime_order_count
FROM
  dash_customer c
  CROSS JOIN LATERAL (
    -- => LATERAL #1 (co-09): the MOST RECENT order, correlated to c.id
    -- This is exactly the top-N-per-group pattern from earlier LATERAL examples
    -- in this topic -- ORDER BY + LIMIT inside a correlated subquery.
    SELECT
      order_date,
      amount
    FROM
      customer_order
    WHERE
    -- The correlation happens HERE -- c.id comes from the outer
    -- dash_customer row currently being processed, which is exactly what
    -- makes this subquery LATERAL rather than an ordinary uncorrelated one.
      customer_id = c.id
    ORDER BY
      order_date DESC
    LIMIT
      -- LIMIT 1 combined with ORDER BY order_date DESC is the standard
      -- top-N-per-group idiom -- exactly one row per customer, guaranteed.
      1
  ) latest
  CROSS JOIN LATERAL (
    -- => LATERAL #2 (co-09): a DIFFERENT correlated shape (an aggregate, not a row)
    -- -- both LATERAL subqueries reference the SAME outer c.id independently
    -- Unlike LATERAL #1, this one always returns EXACTLY one row per customer
    -- (COUNT(*) never returns zero rows) -- both LATERALs happen to be safe to
    -- CROSS JOIN here, but a LATERAL that could return ZERO rows would silently
    -- drop that customer from the final result under CROSS JOIN LATERAL.
    SELECT
      -- Aggregating INSIDE the LATERAL subquery, not in the outer query's
      -- own GROUP BY, is what lets this coexist with LATERAL #1's row-shaped
      -- result in the same SELECT list.
      COUNT(*) AS order_count
    FROM
      customer_order
    WHERE
      customer_id = c.id
  ) stats
ORDER BY
-- ORDER BY here sorts the FINAL 3-row report alphabetically -- it has no
-- bearing on either LATERAL subquery's own internal ORDER BY clause.
  c.name;
-- The final report has exactly 3 rows (one per customer) -- each populated by
-- TWO independent correlated lookups, computed in a single query plan.
