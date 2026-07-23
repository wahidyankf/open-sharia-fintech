-- Example 37: LATERAL Join Top-N.
-- LATERAL (co-09) lets a subquery in FROM reference COLUMNS from an earlier item
-- in the same FROM clause -- here, each author's OWN id feeds their own per-author
-- top-2-books lookup, something a plain JOIN's subquery could never reference.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => resets state -- this example is fully self-contained
-- Same author/book schema as Examples 1-5, with Ada given a THIRD book so her
-- top-2 result visibly EXCLUDES one, unlike Hopper's exactly-2 books.
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
-- Same money-safe NUMERIC precision convention as every book.price column
-- in this topic's earlier examples.
  price NUMERIC(6, 2) NOT NULL,
-- This is the exact FOREIGN KEY the LATERAL WHERE clause below walks --
-- book.author_id = a.id -- the same relationship every join in this topic uses.
  author_id INTEGER REFERENCES author (id)
);

INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace'),
  (2, 'Grace Hopper');

-- Ada's 3 books have 3 distinct prices -- Refactoring and Pragmatic Programmer
-- are her 2 priciest, so Clean Code is the one LATERAL's LIMIT 2 excludes.
INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'The Pragmatic Programmer', 34.99, 1),
  (2, 'Clean Code', 29.99, 1),
  (3, 'Refactoring', 39.99, 1),
  (4, 'The Mythical Man-Month', 24.50, 2),
  (5, 'Peopleware', 22.00, 2);

-- => Ada has 3 books, Hopper has 2 -- top-2-per-author below
-- LATERAL (co-09) lets this subquery reference a.id -- the OUTER author row --
-- something an ordinary FROM-clause subquery is not allowed to do at all.
SELECT
-- a.name is the only column pulled from author itself -- everything else in
-- the output comes from the LATERAL subquery's own result set.
  a.name,
-- top_books.title/price are the LATERAL subquery's own OUTPUT columns --
-- accessible in the outer SELECT exactly like any other joined table's columns.
  top_books.title,
  top_books.price
FROM
-- author a is the DRIVING side of this LATERAL join -- its rows are what get
-- fed, one at a time, into the LATERAL subquery on the right.
  author a
-- CROSS JOIN LATERAL (rather than a plain CROSS JOIN) is what grants the
-- subquery permission to reference a.id -- LATERAL is the keyword that lifts
-- the "subqueries in FROM cannot see sibling FROM items" restriction.
-- CROSS JOIN LATERAL drops an author entirely if their LATERAL subquery
-- returns zero rows -- a LEFT JOIN LATERAL would instead keep the author with
-- NULL book columns, the same INNER-vs-OUTER distinction as any other join.
  CROSS JOIN LATERAL (
-- Conceptually, Postgres re-runs this entire subquery ONCE PER outer author
-- row, substituting that row's a.id each time -- similar in spirit to how a
-- correlated subquery (Example 2) re-evaluates per outer row, but usable in FROM.
    SELECT
      title,
      price
    FROM
      book
    WHERE
-- This is the LATERAL reference itself -- a.id would be completely out of
-- scope here without the LATERAL keyword on the join above.
      book.author_id = a.id -- => the LATERAL reference: a.id from the OUTER row
-- Ordering by price DESC INSIDE the subquery is what determines which 2 books
-- LIMIT keeps -- this ORDER BY is local to the LATERAL subquery, unrelated to
-- the outer query's own final ORDER BY below.
    ORDER BY
      price DESC
-- LIMIT works INSIDE a LATERAL subquery exactly as it would in a standalone
-- query -- LATERAL does not restrict which SQL features are usable within it.
    LIMIT
      2 -- => top 2 per author, computed FRESH for each author row
  ) AS top_books
-- The outer ORDER BY re-sorts the FINAL combined result for display -- each
-- author's own top_books.price DESC ordering was already fixed inside the
-- LATERAL subquery itself, independent of this outer clause.
ORDER BY
  a.name,
  top_books.price DESC;

-- => Ada: Refactoring (39.99), Pragmatic Programmer (34.99) -- Clean Code excluded
-- => Hopper: Mythical Man-Month (24.50), Peopleware (22.00) -- both, only 2 exist
-- Before Postgres 9.3 introduced LATERAL, this exact per-author top-N pattern
-- had no clean SQL expression at all -- it required either a correlated
-- subquery returning an array, or application-side looping.
-- LATERAL composes with any subquery shape -- aggregates, window functions,
-- or (as here) an ORDER BY/LIMIT top-N pattern all work identically.
