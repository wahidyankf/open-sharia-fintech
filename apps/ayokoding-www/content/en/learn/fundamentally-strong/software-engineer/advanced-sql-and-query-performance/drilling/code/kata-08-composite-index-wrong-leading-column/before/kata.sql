-- Kata 8 (before): a composite index's LEADING column doesn't match the query's
-- actual filter, so the B-tree can't be searched efficiently for this query.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL, published_year INTEGER NOT NULL);
INSERT INTO book(id, author_id, published_year)
SELECT n, 1 + (n % 5000), 1990 + (n % 35)
FROM generate_series(1, 200000) AS n;
-- the report always filters by published_year ALONE -- but the index was
-- built leading with author_id, the column the report never filters on solo.
CREATE INDEX idx_book_author_year ON book(author_id, published_year);
ANALYZE book;

-- BUG: no author_id in the WHERE clause -- a B-tree's leading column must be
-- constrained for the tree to narrow the search; published_year alone can only
-- be checked by scanning the WHOLE index (or the whole table), not searched.
EXPLAIN SELECT id FROM book WHERE published_year = 2010;
