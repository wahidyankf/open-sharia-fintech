-- Example 29: Correlated Subquery to Join.
-- Rewriting a correlated subquery (co-01) as an explicit JOIN often gives the
-- planner more freedom to choose a hash or merge strategy instead of a per-row
-- probe (co-24) -- same result set, potentially a very different plan.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;
-- Resetting both tables guarantees this example's row counts are exactly
-- what the comments below describe, regardless of what ran before it.

-- => resets state -- this example is fully self-contained
-- Same author/book schema as Examples 1-5, plus Turing (zero books) reprised
-- from Example 2 -- this dataset is reused deliberately across many examples.
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
-- price is unused by either query form here -- carried over from the shared
-- schema purely for consistency with earlier examples, not because this
-- example needs it.
  price NUMERIC(6, 2) NOT NULL,
-- The same FOREIGN KEY relationship both forms rely on -- Form 1's correlation
-- predicate and Form 2's JOIN condition both walk this exact FK relationship.
  author_id INTEGER REFERENCES author (id)
);

-- => both tables exist, currently empty
-- Turing again seeds the zero-books edge case -- both forms below must agree
-- on excluding him, proving the rewrite preserves EXISTS's exact semantics.
INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace'),
  (2, 'Grace Hopper'),
  (3, 'Alan Turing');

-- Ada has 2 books, Grace has 1, Turing has 0 -- enough variety that a plain
-- JOIN (Form 2) would produce a DIFFERENT row count than EXISTS (Form 1)
-- if DISTINCT were omitted, which is exactly the gotcha this example proves.
INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'The Pragmatic Programmer', 34.99, 1),
  (2, 'Clean Code', 29.99, 1),
  (3, 'The Mythical Man-Month', 24.50, 2);

-- => Turing has zero books -- the anti-join case below
-- Form 1: correlated EXISTS (co-01) -- same shape as Example 2.
-- Form 1 never duplicates a row: EXISTS is a boolean test, so each author
-- appears AT MOST once regardless of how many books they have.
SELECT
  a.name
FROM
  author a
WHERE
  EXISTS (
-- Same idiomatic SELECT 1 as Example 2 -- EXISTS only cares whether a matching
-- row is found, never what that row contains.
    SELECT
      1
    FROM
      book b
    WHERE
      b.author_id = a.id
  )
-- Sorting alphabetically makes the two forms' output trivially comparable
-- side by side -- both forms return "Ada" then "Grace", in that order.
ORDER BY
  a.name;

-- => Ada, Grace -- authors WITH at least one book
-- Form 2: the join rewrite -- DISTINCT because a join duplicates author rows once
-- PER matching book, which EXISTS never did (co-24: a different physical strategy).
-- Ada's 2 books mean the raw JOIN (before DISTINCT) would emit Ada TWICE --
-- once per matching book row -- Grace's 1 book emits her once, and Turing,
-- having zero books, never appears in an INNER JOIN result at all.
SELECT DISTINCT
  a.name
FROM
  author a
-- This ON condition is IDENTICAL to the correlation predicate inside Form 1's
-- EXISTS -- the rewrite is mechanical: move the correlation from a subquery
-- WHERE clause into an explicit JOIN condition.
  JOIN book b ON b.author_id = a.id
-- The SAME ordering as Form 1 -- necessary for a fair side-by-side comparison
-- of the two forms' output, independent of what each form's default row order might be.
ORDER BY
  a.name;

-- => identical 2 rows: Ada, Grace -- same logical result,
-- => but the planner can now choose Hash Join or Merge Join
-- => instead of a per-row correlated subquery probe
-- "Different physical strategy, same logical result" is the running theme this
-- example sets up -- Examples 49-51 show EXPLAIN output proving the planner
-- really does pick different join algorithms (nested loop, hash, merge) for
-- queries shaped like these two forms.
