-- Example 1: Uncorrelated Subquery.
-- A scalar subquery (co-01) runs ONCE, independent of the outer query -- "uncorrelated"
-- means it never references a column from the outer query's own tables.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
-- WARNING (not the default NOTICE) suppresses the routine "table does not exist,
-- skipping" notice that DROP TABLE IF EXISTS prints on a fresh database, while
-- still surfacing genuine warnings and errors if something else goes wrong.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;
-- CASCADE ensures dropping author does not fail if a leftover book row (from a
-- prior interrupted run) still references it via the FOREIGN KEY -- CASCADE drops
-- that dependent constraint along with the table, keeping the reset unconditional.

-- => resets state -- this example is fully self-contained
-- => explicit INTEGER PRIMARY KEY (not SERIAL/IDENTITY) keeps the seed IDs
-- => predictable across every run -- convenient for teaching, not typical production practice
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => author table exists, currently empty
-- price uses NUMERIC(6, 2), not FLOAT/REAL -- exact decimal arithmetic matters for
-- money math; the AVG(price) comparison below must not accumulate binary rounding error.
-- author_id REFERENCES author(id) with no ON DELETE clause defaults to RESTRICT --
-- Postgres blocks deleting an author while their books still reference the row.
CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  price NUMERIC(6, 2) NOT NULL,
  author_id INTEGER REFERENCES author (id)
);

-- => book table exists -- author_id references author(id)
-- Authors must be inserted before books because book.author_id has a FOREIGN KEY
-- constraint referencing author.id -- inserting the child row first would raise a
-- foreign_key_violation; Postgres checks the reference immediately at INSERT time.
INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace'),
  (2, 'Grace Hopper');

-- => 2 authors seeded
-- Three prices are chosen deliberately: 34.99 and 29.99 sit above the eventual
-- average (29.83) while 24.50 sits below it -- guaranteeing the WHERE clause below
-- keeps exactly 2 of 3 rows, a clean teaching split rather than an edge case.
INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'The Pragmatic Programmer', 34.99, 1),
  (2, 'Clean Code', 29.99, 1),
  (3, 'The Mythical Man-Month', 24.50, 2);

-- => 3 books; average price = (34.99+29.99+24.50)/3 = 29.83
-- The subquery (SELECT AVG(price) FROM book) computes exactly ONE number, independent
-- of the outer book row under test -- that single number is reused for every row (co-01).
SELECT
  title,
  price
FROM
  book
WHERE
-- A scalar subquery used with a bare comparison operator (>) must return AT MOST
-- one row and one column -- if AVG(price) matched zero rows it would return NULL
-- and every comparison would be UNKNOWN (no rows returned); if it somehow returned
-- more than one row, Postgres would raise "more than one row returned by a
-- subquery used as an expression".
  price > (
    SELECT
      AVG(price)
    FROM
      book
  );

-- => planner evaluates the subquery once, then filters (co-24)
-- => returns the 2 books priced above the 29.83 average
-- The equivalent join rewrite: compute the average once as a derived table (a subquery
-- used AS a table, co-01), then compare every book row against it via CROSS JOIN.
-- Rewriting a WHERE-clause subquery as a CROSS JOIN derived table matters more
-- once a query needs the SAME aggregate value in several places (SELECT list,
-- WHERE, and ORDER BY) -- the subquery form forces Postgres to either recompute
-- AVG(price) each time or rely on subplan caching, while the CROSS JOIN form
-- computes it exactly once as a named column.
SELECT
  b.title,
  b.price
FROM
  book b
-- Postgres REQUIRES an alias on every derived table (a subquery in FROM/JOIN) --
-- omitting "AS stats" below would raise "subquery in FROM must have an alias".
  CROSS JOIN (
    SELECT
      AVG(price) AS avg_price
    FROM
      book
  ) AS stats
WHERE
  b.price > stats.avg_price;

-- => same 2 rows -- confirms subquery and CROSS JOIN
-- => derived-table forms are semantically interchangeable
-- Semantically interchangeable does NOT always mean cost-identical -- later EXPLAIN
-- examples in this topic show how the planner can choose different execution
-- strategies for logically equivalent subquery and join rewrites.
