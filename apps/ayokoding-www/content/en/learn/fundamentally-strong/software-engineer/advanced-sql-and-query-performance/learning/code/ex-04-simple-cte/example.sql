-- Example 4: Simple CTE.
-- WITH (co-02) names a subquery once, up front, so the main query below can
-- reference it by name -- purely a readability factoring, not a performance change.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => resets state -- this example is fully self-contained
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

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

-- => 3 books seeded -- one below the $25 threshold below
-- expensive_books (co-02) is a named step: the filter logic lives in ONE place,
-- readable top-to-bottom, instead of nested inside the final SELECT's FROM clause.
-- On Postgres 12+, a non-recursive CTE referenced exactly once is, by default,
-- INLINED ("substituted") into the surrounding query just like a plain derived
-- table -- the planner can push the outer join/filter down into it. Writing
-- MATERIALIZED after AS would force it to run standalone and cache its result.
-- This is a NON-recursive CTE -- it runs its inner query exactly once. Example 6
-- introduces WITH RECURSIVE, where the same CTE name can reference itself.
-- The CTE name expensive_books is deliberately descriptive rather than a terse
-- alias like t1 or cte1 -- readability was the entire justification for reaching
-- for WITH over a derived table in the first place, so a vague name would defeat
-- the purpose.
WITH
  expensive_books AS (
    SELECT
      title,
      price,
-- author_id must be carried through the CTE's SELECT list even though the final
-- query never displays it -- a CTE only exposes the columns it explicitly
-- projects, so the join key below would be unavailable if this line were dropped.
      author_id
    FROM
      book
    WHERE
-- The $25 cutoff is chosen so exactly one of the three seeded books (24.50) is
-- excluded -- the CTE is proven to filter, not just rename, the underlying rows.
-- price is NOT NULL, so "price > 25" never has to reckon with a NULL turning
-- the comparison to UNKNOWN -- a nullable price column would need a companion
-- "price IS NOT NULL" or COALESCE to guarantee predictable filtering here.
      price > 25
  )
SELECT
-- expensive_books.title/price are qualified even though no other table in this
-- query has a column of the same name -- qualifying anyway documents provenance
-- and avoids breakage the moment another joined table introduces a same-named column.
  a.name,
  expensive_books.title,
  expensive_books.price
FROM
-- Starting FROM the CTE (not author) means only authors who WROTE a filtered-in
-- book can appear at all -- combined with the plain JOIN below, an author whose
-- only book got filtered out by the CTE's WHERE clause disappears entirely.
  expensive_books
-- Joining on a.id = expensive_books.author_id (rather than the reverse order)
-- reads "filtered books joined back to their authors" -- Postgres does not care
-- about operand order for equality joins; the planner picks its own join order.
  JOIN author a ON a.id = expensive_books.author_id;

-- => The Mythical Man-Month (24.50) is filtered out by the CTE
-- => returns exactly the 2 books priced above $25
-- Contrast with Example 3's derived table: the SQL shape (WITH ... AS vs a
-- subquery in FROM) is almost identical, but naming the step up front reads
-- better once a pipeline chains several such steps (see Example 5, multi-step CTE).
-- CTEs can also encapsulate window functions or aggregates -- this example keeps
-- expensive_books to a plain filter to isolate the WITH syntax itself.
