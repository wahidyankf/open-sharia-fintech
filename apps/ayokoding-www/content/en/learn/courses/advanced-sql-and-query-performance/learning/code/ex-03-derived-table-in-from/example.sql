-- Example 3: Derived Table in FROM.
-- A derived table (co-01) is a subquery given an alias and used exactly like a real
-- table in FROM -- here it pre-aggregates book stats per author before the join.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => resets state -- this example is fully self-contained
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- NUMERIC(6, 2) caps stored prices at 9999.99 -- four digits before the decimal
-- point plus two after; a real catalog would size this per actual business need.
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

-- => Ada: 2 books, Hopper: 1 book -- stats differ per author
-- price_stats is a derived table: GROUP BY collapses book rows to one row per
-- author_id BEFORE the outer join ever sees them (co-01). ROUND keeps output tidy.
-- Aggregation MUST happen inside the derived table, not the outer query -- you
-- cannot JOIN directly on COUNT(*)/AVG(price) without first collapsing book rows
-- to one row per author_id; the derived table is exactly that collapsing step.
SELECT
  a.name,
-- Selecting from author (not book) as the driving table, combined with a plain
-- JOIN (not LEFT JOIN), means any author with zero books would silently vanish
-- from the result -- fine here since both seeded authors have at least one book,
-- but worth remembering: a plain JOIN never surfaces the zero-match case.
  price_stats.book_count,
  price_stats.avg_price
FROM
  author a
  JOIN (
-- COUNT(*) counts ROWS, including any with NULL columns -- COUNT(price) would
-- instead count only non-NULL price values, which matters once nullable columns
-- enter the picture (price is NOT NULL here, so the two forms happen to agree).
    SELECT
      author_id,
      COUNT(*) AS book_count,
-- ROUND(..., 2) matches the NUMERIC(6, 2) precision of price -- AVG() on a
-- NUMERIC column already returns exact decimal arithmetic, unlike AVG() on a
-- FLOAT/REAL column, which could reintroduce binary rounding error here.
      ROUND(AVG(price), 2) AS avg_price
    FROM
      book
-- Grouping by author_id (the foreign key), not id (book's own primary key), is
-- what collapses multiple book rows per author into a single summary row --
-- grouping by id instead would produce one output row per BOOK, not per author.
    GROUP BY
      author_id
-- price_stats.author_id has no index of its own -- it is a derived, in-memory
-- result set, not a real table -- but the underlying GROUP BY over book can still
-- benefit from an index on book.author_id if one exists (see Example 21).
-- For an INNER JOIN, moving this condition from ON into a WHERE clause instead
-- would produce an identical result -- the ON/WHERE distinction only changes
-- outcomes once an OUTER JOIN (LEFT/RIGHT/FULL) is introduced.
  ) AS price_stats ON price_stats.author_id = a.id;

-- => Ada: book_count 2, avg_price (34.99+29.99)/2 = 32.49
-- => Hopper: book_count 1, avg_price 24.50
-- Unlike a CTE (see Example 4), the planner is free to "flatten" this derived
-- table into the surrounding query -- pushing the author filter/join condition
-- down before aggregating -- because a plain subquery is not an optimization fence.
