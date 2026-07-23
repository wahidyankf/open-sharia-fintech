-- Example 44: Hash Index.
-- USING hash (co-20) builds a hash table instead of a sorted B-tree -- it supports
-- EQUALITY lookups only (no <, >, BETWEEN, no ORDER BY support), but each lookup
-- is a single hash computation rather than a tree descent.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS customer CASCADE;

-- => resets state -- this example is fully self-contained
-- Same generate_series-seeded customer table pattern as Example 43 -- this time
-- with consistently lower-case emails, since the point here is index TYPE, not
-- case-insensitivity.
CREATE TABLE customer (id INTEGER PRIMARY KEY, email TEXT NOT NULL);

-- Every email is unique (n is the series' own row number), which is exactly
-- the access pattern a hash index is built for: point lookups by exact key.
INSERT INTO
  customer (id, email)
SELECT
  n,
  'user' || n || '@example.com'
FROM
  generate_series (1, 100000) AS n;

-- => 100,000 rows -- email is unique per row, ideal for equality lookups
-- CREATE INDEX ... USING hash (co-20) -- explicitly requests a hash index over a
-- B-tree, appropriate here because THIS column is only ever queried by exact match.
-- USING hash is the ONLY part that differs from a plain CREATE INDEX -- omitting
-- it (as in Example 21) would default to a B-tree, which ALSO supports equality
-- but additionally supports ordering and range predicates a hash index cannot.
CREATE INDEX idx_customer_email_hash ON customer USING hash (email);

-- Refreshing statistics here matters just as much as it did for the B-tree
-- and expression-index examples -- the planner needs current selectivity
-- estimates to decide between the new hash index and a sequential scan.
ANALYZE customer;

-- Equality (=) can use a hash index -- this is the ONLY predicate shape it supports.
-- A single hash-table lookup, not a multi-level tree descent, is what makes
-- hash index equality lookups theoretically cheaper than B-tree ones at very
-- large table sizes -- the tradeoff is losing ordering/range support entirely.
EXPLAIN
SELECT
  id
FROM
  customer
WHERE
  email = 'user50000@example.com';

-- => Index Scan using idx_customer_email_hash -- equality served directly
-- A range predicate CANNOT use a hash index at all -- there is no B-tree ordering
-- to walk -- so the planner falls back to a sequential scan for this shape.
-- This is the DIRECT tradeoff hash indexes make: gaining O(1)-ish equality
-- lookups costs you EVERY other predicate shape a B-tree would have served --
-- less than, greater than, BETWEEN, LIKE 'prefix%', and ORDER BY all fall back
-- to a full scan here.
EXPLAIN
SELECT
  id
FROM
  customer
WHERE
  email > 'user50000@example.com';

-- => Seq Scan on customer -- the hash index is structurally unusable here
