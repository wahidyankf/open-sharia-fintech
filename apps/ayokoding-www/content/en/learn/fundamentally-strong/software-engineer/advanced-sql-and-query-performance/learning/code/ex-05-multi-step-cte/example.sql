-- Example 5: Multi-Step CTE.
-- Chaining CTEs (co-02) stages a transform: each step consumes the one before it,
-- turning one dense query into a readable pipeline of named intermediate results.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => resets state -- this example is fully self-contained
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- The same author/book schema as Examples 1-4 -- reused deliberately so this
-- example can focus entirely on the CTE-chaining pattern, not new table shapes.
CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  price NUMERIC(6, 2) NOT NULL,
  author_id INTEGER REFERENCES author (id)
);

-- => both tables exist, currently empty
INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace'),
  (2, 'Grace Hopper');

INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'The Pragmatic Programmer', 34.99, 1),
  (2, 'Clean Code', 29.99, 1),
  (3, 'The Mythical Man-Month', 24.50, 2);

-- => Ada's avg (34.99+29.99)/2=32.49; Hopper's avg 24.50
-- Step 1: per-author totals. Step 2: the overall average book price (one row).
-- Step 3: authors whose OWN average exceeds the overall average -- each step
-- builds on the last, exactly like a small data pipeline (co-02).
WITH
-- Step 1 groups book rows into one row per author (same shape as the derived
-- table in Example 3) -- book_count rides along even though this example never
-- uses it downstream, showing a CTE step can expose more than later steps need.
  book_totals AS (
    SELECT
      author_id,
      COUNT(*) AS book_count,
-- ROUND(..., 2) is applied independently in steps 1 and 2 -- each step rounds
-- its own average, so the step-3 comparison is between two consistently-rounded
-- NUMERIC(6, 2) values rather than one rounded and one raw high-precision average.
      ROUND(AVG(price), 2) AS avg_price
    FROM
      book
-- GROUP BY author_id here plays the identical role it played in Example 3's
-- derived table -- collapsing per-book rows to per-author rows before anything
-- downstream can compare authors against each other.
    GROUP BY
      author_id
  ),
-- Step 2 computes a SINGLE overall number with no GROUP BY at all -- an aggregate
-- with no GROUP BY always collapses the WHOLE table to exactly one row, which is
-- exactly what step 3 needs to compare every author's average against. A window
-- function AVG(price) OVER () (see Example 9) could compute this inline instead.
  overall_avg AS (
    SELECT
-- Renaming overall_avg_price (rather than reusing avg_price) avoids ambiguity
-- in step 3's WHERE clause -- Postgres would otherwise require additional
-- qualification to disambiguate two identically named avg_price columns.
      ROUND(AVG(price), 2) AS overall_avg_price
    FROM
      book
  ),
-- Step 3 compares step 1's per-author average against step 2's single overall
-- number -- this is the payoff of chaining CTEs: each step only has to reason
-- about ONE transformation, not the whole pipeline at once.
  above_average_authors AS (
    SELECT
      book_totals.author_id,
      book_totals.avg_price
    FROM
-- "FROM book_totals, overall_avg" is old-style comma-join syntax, equivalent to
-- an unconditional CROSS JOIN -- safe here ONLY because overall_avg always
-- produces exactly one row (step 2's aggregate has no GROUP BY), so every
-- book_totals row is paired with that single row, not multiplied out. Modern style
-- prefers an explicit CROSS JOIN (see Example 1) to make that guarantee visible.
      book_totals,
      overall_avg
    WHERE
-- Both sides of this comparison already carry NUMERIC(6, 2)-derived precision
-- from ROUND(AVG(price), 2) in steps 1 and 2, so "greater than" compares exact
-- decimal values -- no floating-point tie-breaking surprises at the boundary.
      book_totals.avg_price > overall_avg.overall_avg_price
  )
-- The final SELECT re-joins author because none of the three CTE steps carry
-- the author's name forward -- only author_id survives the aggregation steps;
-- a name column would have needed GROUP BY author_id, name in step 1 instead.
SELECT
  a.name,
-- above_average_authors.avg_price is selected directly -- no re-aggregation is
-- needed here because step 3 already reduced the data to one row per qualifying
-- author.
  above_average_authors.avg_price
FROM
  above_average_authors
-- Joining on a.id = above_average_authors.author_id mirrors Example 4's pattern
-- -- once the interesting authors are isolated, a single equality join recovers
-- their display name from the author table.
  JOIN author a ON a.id = above_average_authors.author_id;

-- => overall avg is (34.99+29.99+24.50)/3 = 29.83
-- => only Ada's 32.49 beats that -- Hopper's 24.50 does not
-- Each CTE here only references the ones ABOVE it (book_totals feeds
-- above_average_authors; overall_avg does too) -- WITH evaluates top-to-bottom
-- and, without RECURSIVE, a step can never reference one defined later.
-- No index exists on book.author_id in this example -- with only 3 rows the
-- planner correctly prefers a sequential scan; Example 40 revisits this same
-- kind of grouping query at a scale where an index actually changes the plan.
