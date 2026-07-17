-- Example 16: Grouping Sets.
-- GROUPING SETS (co-08) lists exactly the groupings you want -- no automatic
-- roll-up hierarchy -- so you can mix independent totals in ONE result set.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS sale CASCADE;

-- => resets state -- this example is fully self-contained
-- Same sale schema and same 4 seed rows as Example 15 -- deliberately identical,
-- so the difference in OUTPUT below is attributable entirely to GROUPING SETS
-- vs ROLLUP, not to any change in the underlying data.
CREATE TABLE sale (
  id INTEGER PRIMARY KEY,
  region TEXT NOT NULL,
  category TEXT NOT NULL,
  amount NUMERIC(8, 2) NOT NULL
);

-- => sale table exists, currently empty
INSERT INTO
  sale (id, region, category, amount)
VALUES
  (1, 'East', 'Books', 100.00),
  (2, 'East', 'Games', 50.00),
  (3, 'West', 'Books', 80.00),
  (4, 'West', 'Games', 40.00);

-- => same 4 rows as Example 15 -- different grouping request
-- GROUPING SETS((region), (category), ()) (co-08) asks for exactly THREE groupings:
-- totals by region, totals by category, and one grand total -- no per-cell detail rows.
-- A single GROUP BY GROUPING SETS(...) still scans the sale table only ONCE --
-- the same single-pass efficiency ROLLUP offers, just with full control over
-- exactly which combinations of columns get their own subtotal row.
SELECT
  region,
  category,
  SUM(amount) AS total
FROM
  sale
-- Each parenthesized entry is one INDEPENDENT grouping: (region) groups by region
-- alone, (category) by category alone, () is the empty grouping -- the grand
-- total with no GROUP BY columns at all. None of the three implies the others.
-- Unlike ROLLUP, GROUPING SETS never implies a hierarchy between its entries --
-- swapping the order of (region), (category), () changes nothing about which
-- rows appear, only (via ORDER BY) their display order.
GROUP BY
  GROUPING SETS ((region), (category), ())
-- NULLS LAST is needed for the same reason as Example 15 -- every grouping set
-- that OMITS a column fills it with NULL in the output, and Postgres defaults
-- to sorting NULLs first unless told otherwise.
ORDER BY
  region NULLS LAST,
  category NULLS LAST;

-- => 2 region-total rows + 2 category-total rows + 1 grand total
-- => NO region+category detail rows -- ROLLUP would have included them
-- ROLLUP(region, category) is actually shorthand for a SPECIFIC grouping-sets
-- list: GROUPING SETS((region, category), (region), ()) -- GROUPING SETS is the
-- more general primitive; ROLLUP and CUBE are convenience syntax built on top of it.
