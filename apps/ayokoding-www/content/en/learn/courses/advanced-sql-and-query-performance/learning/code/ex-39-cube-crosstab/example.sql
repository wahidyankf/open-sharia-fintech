-- Example 39: CUBE Crosstab.
-- CUBE(region, category) (co-08) produces EVERY combination of subtotals: the full
-- cross-tabulation, both single-dimension totals, AND the grand total -- ROLLUP's
-- fixed hierarchy is a STRICT SUBSET of what CUBE computes.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS sale CASCADE;

-- => resets state -- this example is fully self-contained
-- Identical schema and seed data to Examples 15 and 16 -- CUBE, ROLLUP, and
-- GROUPING SETS are compared fairly against the exact same 4 rows.
CREATE TABLE sale (
  id INTEGER PRIMARY KEY,
-- region and category are BOTH included in CUBE's argument list -- CUBE(region)
-- alone would instead just produce region subtotals plus a grand total.
  region TEXT NOT NULL,
  category TEXT NOT NULL,
-- Same amount column and NOT NULL constraint as Examples 15/16 -- reused
-- verbatim so this example's ONLY new concept is the CUBE keyword itself.
  amount NUMERIC(8, 2) NOT NULL
);

-- The same 2-region, 2-category, 4-row dataset -- small enough that all 9
-- CUBE output rows can be eyeballed directly against the raw input.
INSERT INTO
  sale (id, region, category, amount)
VALUES
  (1, 'East', 'Books', 100.00),
  (2, 'East', 'Games', 50.00),
  (3, 'West', 'Books', 80.00),
  (4, 'West', 'Games', 40.00);

-- => same 4-row dataset as Examples 15/16 -- compare all three outputs
-- CUBE(region, category) (co-08) = detail rows + region subtotals + category
-- subtotals + grand total -- ROLLUP only gave detail + region subtotals + grand total.
SELECT
  region,
  category,
-- The single SUM(amount) aggregate is unchanged from Examples 15/16 -- only
-- the grouping construct (CUBE here) differs across the three examples.
  SUM(amount) AS total
FROM
  sale
-- CUBE(region, category) is shorthand for the FULL grouping-sets list:
-- GROUPING SETS((region, category), (region), (category), ()) -- all FOUR
-- combinations of the two columns, including both included and both excluded.
GROUP BY
  CUBE (region, category)
-- NULLS LAST is required for the same reason as Examples 15 and 16 -- every
-- omitted-column combination fills that column with NULL in CUBE's output.
ORDER BY
  region NULLS LAST,
  category NULLS LAST;

-- => 4 detail + 2 region subtotals + 2 category subtotals + 1 grand total = 9 rows
-- => (ROLLUP produced 7, GROUPING SETS produced 5 -- CUBE is the superset)
-- CUBE grows FAST with more columns -- CUBE(a, b, c) produces 2^3 = 8
-- groupings, not 4 -- reach for GROUPING SETS directly once only a handful of
-- the full combinatorial set is actually needed.
