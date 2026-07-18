-- Example 17: FILTER Aggregate.
-- FILTER (WHERE ...) (co-10) restricts what ONE aggregate call counts, letting
-- several differently-filtered aggregates run side by side in a single query pass.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS sale CASCADE;

-- => resets state -- this example is fully self-contained
-- No region column this time -- category alone is enough to demonstrate FILTER,
-- since the point here is comparing aggregates, not grouping dimensions.
CREATE TABLE sale (
  id INTEGER PRIMARY KEY,
-- category is NOT NULL -- FILTER's WHERE clause never has to reckon with a NULL
-- category turning the comparison to UNKNOWN and silently excluding a row.
  category TEXT NOT NULL,
  amount NUMERIC(8, 2) NOT NULL
);

-- => sale table exists, currently empty
-- 3 Books rows and 2 Games rows -- an intentionally uneven split so
-- books_via_filter (3) is visibly different from total_rows (5).
INSERT INTO
  sale (id, category, amount)
VALUES
  (1, 'Books', 100.00),
  (2, 'Games', 50.00),
  (3, 'Books', 80.00),
  (4, 'Games', 40.00),
  (5, 'Books', 20.00);

-- => 5 rows: 3 Books, 2 Games
-- COUNT(*) FILTER (WHERE category = 'Books') (co-10) counts ONLY rows matching the
-- filter -- the plain COUNT(*) alongside it still counts every row, unfiltered.
SELECT
  COUNT(*) AS total_rows,
-- FILTER (WHERE ...) is SQL-standard syntax attached directly to an aggregate
-- call -- it only affects THAT aggregate, unlike a query-level WHERE clause,
-- which would filter every row (and every aggregate) before aggregation even starts.
  COUNT(*) FILTER (
    WHERE
      category = 'Books'
  ) AS books_via_filter,
-- COUNT(expr) counts only NON-NULL values of expr -- the CASE here has no ELSE,
-- so non-Books rows evaluate to NULL and are silently excluded from the count.
-- This CASE trick predates FILTER (added in SQL:2003 vs FILTER's SQL:2011) and
-- still appears constantly in codebases and engines without FILTER support.
  COUNT(
    CASE
      WHEN category = 'Books' THEN 1
    END
  ) AS books_via_case
FROM
-- All three aggregates run in a SINGLE pass over sale -- FILTER and the CASE
-- trick both avoid the need for three separate queries (or a self-join) to
-- get an overall count alongside a conditionally-filtered one.
  sale;

-- => total_rows 5 -- every row, no filtering at all
-- => books_via_filter 3 -- FILTER and CASE agree exactly
-- => books_via_case 3 -- the older, more verbose equivalent
-- FILTER is generally preferred over the CASE trick when available: it reads
-- as "count these, filtered by this condition" directly, rather than requiring
-- the reader to notice a deliberately-omitted ELSE and infer NULL-counting behavior.
