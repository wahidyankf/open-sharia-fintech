-- Example 38: LATERAL vs Correlated Subquery.
-- A correlated scalar subquery in the SELECT list (co-01) and a LEFT JOIN LATERAL
-- (co-09) can express the SAME "one related row per outer row" query -- but only
-- LATERAL can return MULTIPLE columns from that related row in one join.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;
-- Resetting both tables first keeps the row counts in every comment below
-- accurate regardless of what ran before this script.

-- => resets state -- this example is fully self-contained
-- Same author/book schema as Examples 1-5, with Ada given a second book and
-- Turing reprising his zero-books role from Example 2 -- both forms below must
-- agree on how they handle Turing.
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
-- Same money-safe NUMERIC precision convention as this topic's other
-- book.price columns.
  price NUMERIC(6, 2) NOT NULL,
-- The same author/book FK relationship every correlated query in this topic
-- walks -- Form 1 and Form 2 both filter on it identically.
  author_id INTEGER REFERENCES author (id)
);

INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace'),
  (2, 'Grace Hopper'),
  (3, 'Alan Turing');

-- Ada's two books have different prices -- Refactoring (39.99) outranks
-- Pragmatic Programmer (34.99), so Refactoring is the one "top_book" both
-- forms below should agree on.
INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'The Pragmatic Programmer', 34.99, 1),
  (2, 'Refactoring', 39.99, 1),
  (3, 'The Mythical Man-Month', 24.50, 2);

-- => Turing has ZERO books -- the outer-join case both forms must handle
-- Form 1: a correlated scalar subquery (co-01) -- limited to exactly ONE column.
-- The parenthesized subquery here sits directly in the SELECT list, as if it
-- were an ordinary scalar expression -- Postgres requires it to return AT MOST
-- one row and one column, exactly like the scalar subquery gotcha in Example 1.
SELECT
  a.name,
  (
-- Only ONE column (title) can be projected here -- adding a second column
-- would make this an invalid scalar subquery, raising a syntax/type error.
    SELECT
      title
    FROM
      book
    WHERE
-- This correlation is structurally identical to Example 2's EXISTS subquery --
-- a.id reaches into the outer author row from inside the correlated subquery.
      book.author_id = a.id
-- ORDER BY price DESC LIMIT 1 is what turns "all of this author's books" into
-- "the single highest-priced one" -- LIMIT 1 is what guarantees the scalar
-- subquery's one-row requirement is actually satisfied, not just hoped for.
    ORDER BY
      price DESC
    LIMIT
      1
  ) AS top_book
FROM
-- No JOIN at all is needed for Form 1 -- the correlated subquery embedded in
-- the SELECT list implicitly runs once per author row, achieving the same
-- "one row per author, even with zero books" outcome an OUTER JOIN would need.
  author a
ORDER BY
  a.name;

-- => Turing: top_book is NULL -- a scalar subquery with zero
-- => matching rows naturally returns NULL, no outer-join syntax needed
-- A scalar subquery naturally behaves like an OUTER join for the "row exists
-- or not" question -- Turing gets a row with NULL, never gets dropped, with
-- zero extra join syntax required.
-- Form 2: LEFT JOIN LATERAL (co-09) -- can return SEVERAL columns (title AND
-- price here), which a scalar subquery could never do in one expression.
-- Form 2 repeats the EXACT SAME correlated filter/order/limit logic as Form 1's
-- subquery, just written as a LATERAL subquery in FROM instead of in SELECT.
SELECT
-- top.title and top.price are both pulled from the SAME single matched row --
-- LATERAL's subquery runs once per author, same as Form 1, but can hand back
-- its ENTIRE row shape instead of being squeezed through one scalar value.
  a.name,
  top.title AS top_book,
  top.price AS top_price
FROM
  author a
-- LEFT (not INNER) JOIN LATERAL is what keeps Turing's author row when his
-- LATERAL subquery returns zero books -- an INNER JOIN LATERAL would silently
-- drop Turing entirely, the opposite of what Form 1's scalar subquery does.
  LEFT JOIN LATERAL (
-- Both title AND price are projected here -- LATERAL has no scalar-subquery
-- restriction on column count, which is this whole example's payoff.
    SELECT
      title,
      price
    FROM
      book
    WHERE
-- The identical correlation predicate as Form 1 -- LATERAL's a.id reference
-- works the same way a correlated subquery's does, just inside a FROM clause.
      book.author_id = a.id
-- Same ORDER BY price DESC LIMIT 1 as Form 1 -- LATERAL does not require
-- LIMIT 1 the way a scalar subquery does, but keeping it here preserves the
-- "exactly one top book per author" semantics both forms are comparing.
    ORDER BY
      price DESC
    LIMIT
      1
-- "ON TRUE" is a deliberately trivial join condition -- the REAL correlation
-- already happened inside the LATERAL subquery's own WHERE clause; ON TRUE
-- just satisfies JOIN's syntactic requirement for SOME condition.
  ) AS top ON TRUE
ORDER BY
  a.name;

-- => identical top_book column to Form 1 -- PLUS top_price, a
-- => second column the scalar-subquery form structurally cannot provide
-- => LEFT JOIN ... ON TRUE (not CROSS JOIN) keeps Turing's row with NULLs
-- The general rule: reach for a correlated scalar subquery when exactly ONE
-- column is needed, and for LATERAL the moment a SECOND column, an aggregate
-- over several rows, or a LIMIT-based top-N shape is required instead.
