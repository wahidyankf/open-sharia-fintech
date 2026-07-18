-- Kata 8 (after): a dedicated index with published_year LEADING makes the
-- report's actual filter pattern searchable.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL, published_year INTEGER NOT NULL);
INSERT INTO book(id, author_id, published_year)
SELECT n, 1 + (n % 5000), 1990 + (n % 35)
FROM generate_series(1, 200000) AS n;
CREATE INDEX idx_book_author_year ON book(author_id, published_year);
-- THE FIX: a SEPARATE index (co-19) with published_year as the leading (and
-- only) column -- the composite index above stays for queries that DO filter
-- by author_id first; this one exists for the report's actual access pattern.
CREATE INDEX idx_book_year ON book(published_year);
ANALYZE book;

EXPLAIN SELECT id FROM book WHERE published_year = 2010;
