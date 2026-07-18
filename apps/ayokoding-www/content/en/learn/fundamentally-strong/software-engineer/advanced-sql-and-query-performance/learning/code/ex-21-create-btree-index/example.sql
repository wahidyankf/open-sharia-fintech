-- Example 21: Create B-tree Index.
-- CREATE INDEX (co-18) builds a sorted, separate on-disk structure over a column --
-- B-tree is PostgreSQL's default index type, good for equality AND range queries.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS book,
author CASCADE;

-- => resets state -- this example is fully self-contained
-- The same author/book schema from Examples 1-5 -- reused here so the CREATE
-- INDEX statement below is the ONLY new concept this example introduces.
CREATE TABLE author (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  price NUMERIC(6, 2) NOT NULL,
  author_id INTEGER REFERENCES author (id)
);

-- => both tables exist, currently empty
-- A single book row is deliberately enough -- this example is about proving an
-- index exists and inspecting its catalog entry, not about query results over
-- a meaningfully sized dataset (Example 22 onward uses much larger tables for that).
INSERT INTO
  author (id, name)
VALUES
  (1, 'Ada Lovelace');

INSERT INTO
  book (id, title, price, author_id)
VALUES
  (1, 'Clean Code', 29.99, 1);

-- => a minimal seed -- this example is about the index, not data
-- CREATE INDEX <name> ON <table>(<column>) (co-18) builds a B-tree over book.price --
-- PostgreSQL names it explicitly here rather than relying on the auto-generated name.
-- CREATE INDEX defaults to the B-tree access method when none is specified --
-- writing this as CREATE INDEX ... USING btree ... ON book(price) would be
-- exactly equivalent; B-tree is the right default for equality and range
-- predicates alike (=, <, >, BETWEEN, ORDER BY).
CREATE INDEX idx_book_price ON book (price);

-- => the index now exists as a separate on-disk structure
-- pg_indexes (a system catalog view) proves the index was actually created and
-- shows the exact CREATE INDEX statement PostgreSQL stored for it.
-- pg_indexes is a convenience VIEW over the lower-level pg_index/pg_class system
-- catalogs -- it joins them together and formats the index definition as
-- ready-to-read DDL text, rather than requiring manual catalog joins.
SELECT
  indexname,
  indexdef
FROM
  pg_indexes
-- pg_indexes is NOT scoped to one table by default -- it lists every index in
-- the current database across every table, so this WHERE clause is what narrows
-- the result down to book's indexes specifically.
WHERE
  tablename = 'book'
ORDER BY
  indexname;

-- => 2 indexes: the PRIMARY KEY's auto-created index, and idx_book_price
-- The auto-created PRIMARY KEY index already existed before this script ran
-- CREATE INDEX at all -- declaring PRIMARY KEY implicitly builds a unique
-- B-tree index on that column; idx_book_price is the ONLY index this script
-- explicitly created.
