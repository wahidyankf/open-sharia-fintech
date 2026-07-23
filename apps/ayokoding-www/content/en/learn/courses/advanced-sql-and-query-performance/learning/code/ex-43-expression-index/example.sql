-- Example 43: Expression Index.
-- An expression index (co-21) indexes the OUTPUT of a function or expression, not
-- a raw column -- here, lower(email), so a case-insensitive lookup can use an index
-- even though the stored email values themselves keep their original casing.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS customer CASCADE;

-- => resets state -- this example is fully self-contained
-- A single wide table (100,000 rows) is generated below purely to give EXPLAIN
-- something realistic to reason about -- see Example 22 for the same generator pattern.
CREATE TABLE customer (id INTEGER PRIMARY KEY, email TEXT NOT NULL);

-- 'User' || n || '@Example.com' -- capitalized deliberately so every stored
-- email has mixed case, making a case-sensitive plain index useless for a
-- case-insensitive lookup.
INSERT INTO
  customer (id, email)
SELECT
  n,
  'User' || n || '@Example.com'
FROM
  generate_series (1, 100000) AS n;

-- => emails stored with MIXED case on purpose -- 'User1@Example.com'
-- CREATE INDEX ... (lower(email)) (co-21) indexes lower(email), NOT email itself --
-- a plain index on email cannot serve a lower(email) = ... predicate at all.
-- Postgres computes lower(email) for every EXISTING row once, at index-build
-- time, then keeps it up to date incrementally on every future INSERT/UPDATE --
-- the expression is not re-evaluated at query time from a plain column index.
CREATE INDEX idx_customer_email_lower ON customer (lower(email));

-- ANALYZE refreshes the planner's statistics -- without it, the planner might
-- still choose a sequential scan simply because it doesn't yet know how
-- selective this new expression index actually is.
ANALYZE customer;

-- The query's WHERE clause must match the INDEXED EXPRESSION exactly: lower(email),
-- not email itself, for the planner to recognize it can use this index (co-21).
-- EXPLAIN alone (no ANALYZE) shows the planner's CHOSEN plan and its cost
-- ESTIMATE without actually running the query -- Example 23 contrasts this
-- with EXPLAIN ANALYZE, which executes the query and reports real timings.
EXPLAIN
SELECT
  id,
  email
FROM
  customer
WHERE
  lower(email) = 'user50000@example.com';

-- => Index Scan using idx_customer_email_lower -- the expression matched
-- => a plain WHERE email = 'user50000@example.com' (no lower()) would
-- => NOT match this index -- the stored email is 'User50000@Example.com'
