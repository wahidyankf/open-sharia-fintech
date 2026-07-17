-- Example 18: Conditional SUM (CASE Pivot).
-- SUM(CASE WHEN ... THEN amount ELSE 0 END) (co-10) pivots category values into
-- separate COLUMNS -- one row per region, one column per category, ELSE 0 protects the SUM.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS sale CASCADE;

-- => resets state -- this example is fully self-contained
-- Same region/category/amount shape as Examples 15-16 -- this time pivoted into
-- columns instead of rolled up into subtotal rows, a different way to slice
-- the identical two-dimensional data.
CREATE TABLE sale (
  id INTEGER PRIMARY KEY,
  region TEXT NOT NULL,
  category TEXT NOT NULL,
-- amount is NOT NULL and always non-negative in this seed data -- ELSE 0 stays
-- a safe "no contribution" sentinel because it can never collide with a real
-- negative amount that would need to be distinguished from "filtered out".
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

-- => 4 rows across 2 regions x 2 categories
-- Each CASE (co-10) tests category and contributes amount ONLY on a match --
-- ELSE 0 is essential: without it, SUM would treat non-matching rows as NULL and
-- PostgreSQL's SUM silently skips NULLs, which would still work here but is fragile.
-- This is the classic "pivot" idiom: GROUP BY the row dimension (region), then
-- one SUM(CASE ...) expression PER desired output column (Books, Games) turns
-- category VALUES into column HEADERS -- something GROUP BY alone cannot do.
SELECT
  region,
  SUM(
    CASE
      WHEN category = 'Books' THEN amount
-- ELSE 0 (rather than omitting ELSE) makes every row contribute EXACTLY 0 or
-- amount to books_total -- omitting ELSE would make non-Books rows evaluate to
-- NULL, which SUM also skips, giving the identical result here but relying on
-- SUM's NULL-skipping behavior instead of stating the intent explicitly.
      ELSE 0
    END
  ) AS books_total,
-- games_total repeats the exact same CASE pattern with the condition flipped --
-- each additional category in a real dataset would need its own repeated
-- SUM(CASE...) column, which is this technique's main scaling weakness.
  SUM(
    CASE
      WHEN category = 'Games' THEN amount
      ELSE 0
    END
  ) AS games_total
FROM
-- Every row is scanned by BOTH CASE expressions -- Postgres does not skip the
-- Games check for a Books row or vice versa; each CASE independently decides
-- whether to contribute its own row's amount.
  sale
-- GROUP BY region alone (not region, category) is what collapses East's two
-- rows (Books 100, Games 50) into one output row with both pivoted totals
-- side by side -- grouping by category too would defeat the whole pivot.
GROUP BY
  region
-- ORDER BY region only re-sorts the already-pivoted 2-row result for display --
-- East/West's books_total and games_total values were fixed by GROUP BY, not by
-- this final ordering step.
ORDER BY
  region;

-- => East: books_total 100.00, games_total 50.00
-- => West: books_total 80.00, games_total 40.00
-- Contrast with crosstab()/tablefunc (Example 39): this manual CASE-pivot
-- approach needs one hand-written column per category and breaks once a new
-- category appears, while crosstab() can generate columns more dynamically.
