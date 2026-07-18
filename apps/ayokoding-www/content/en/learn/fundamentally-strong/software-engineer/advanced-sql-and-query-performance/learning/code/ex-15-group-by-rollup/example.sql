-- Example 15: GROUP BY ROLLUP.
-- ROLLUP(region, category) (co-08) produces the normal per-(region,category) groups
-- PLUS a subtotal per region PLUS one grand total -- three levels in a single pass.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS sale CASCADE;

-- => resets state -- this example is fully self-contained
-- region/category are plain TEXT dimensions -- ROLLUP works with any GROUP BY
-- column list, not just two; each extra column adds one more subtotal level.
CREATE TABLE sale (
  id INTEGER PRIMARY KEY,
  region TEXT NOT NULL,
  category TEXT NOT NULL,
-- amount is NOT NULL, so SUM never has to special-case a missing value while
-- rolling up -- a nullable amount would still SUM correctly (NULLs are skipped).
  amount NUMERIC(8, 2) NOT NULL
);

-- => sale table exists, currently empty
-- Two regions, two categories, one row per combination -- the smallest dataset
-- that still produces a distinct subtotal per region under ROLLUP.
INSERT INTO
  sale (id, region, category, amount)
VALUES
  (1, 'East', 'Books', 100.00),
  (2, 'East', 'Games', 50.00),
  (3, 'West', 'Books', 80.00),
  (4, 'West', 'Games', 40.00);

-- => 4 rows across 2 regions x 2 categories
-- ROLLUP(region, category) (co-08) rolls up right-to-left: full detail rows first,
-- then region subtotals (category = NULL), then one grand total (both NULL).
SELECT
  region,
  category,
-- SUM(amount) is the only aggregate here, but ROLLUP composes with COUNT(*),
-- AVG(), or several aggregates side by side -- the rollup mechanics don't care
-- how many aggregate columns ride along in the SELECT list.
  SUM(amount) AS total
FROM
  sale
-- Argument ORDER matters: ROLLUP(region, category) subtotals region first (the
-- LEFTMOST column), then rolls all the way up to a grand total -- ROLLUP(category,
-- region) would instead produce category subtotals, a different hierarchy.
GROUP BY
  ROLLUP (region, category)
-- NULLS LAST is required here because ROLLUP represents a subtotal/grand-total
-- row by putting an actual NULL in the rolled-up column -- without NULLS LAST,
-- Postgres's default NULLS FIRST would sort those summary rows to the TOP.
ORDER BY
  region NULLS LAST,
  category NULLS LAST;

-- => 4 detail rows + 2 region subtotals + 1 grand total = 7 rows
-- => grand total row: region NULL, category NULL, total 270.00
-- The 4 detail rows plus 3 summary rows all come from ONE table scan and ONE
-- aggregation pass -- computing the same three levels with separate GROUP BY
-- queries UNIONed together would scan the table three times instead.
