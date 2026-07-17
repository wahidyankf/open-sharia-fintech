-- Example 24: Seq Scan vs Index Scan.
-- The SAME query, run twice: once with no index (Seq Scan, co-18) and once after
-- adding a targeted B-tree index -- the planner switches strategy on its own (co-24).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL, published_year INTEGER NOT NULL);
INSERT INTO book_catalog(id, isbn, price, published_year)
SELECT n, 'ISBN-' || LPAD(n::TEXT, 9, '0'), (10 + (n % 90))::NUMERIC, 2000 + (n % 25)
FROM generate_series(1, 100000) AS n;
ANALYZE book_catalog;
                                    -- => 100,000 rows, stats fresh -- a fair "before" baseline

-- BEFORE: no index on isbn -- the planner has no faster option than scanning
-- every row (co-24).
EXPLAIN SELECT * FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => Seq Scan on book_catalog -- must check all 100,000 rows

-- Now add the index (co-18) and refresh stats so the planner knows it exists.
CREATE INDEX idx_book_catalog_isbn ON book_catalog(isbn);
ANALYZE book_catalog;
                                    -- => a sorted B-tree over isbn now exists

-- AFTER: same exact query, but the planner now has a much cheaper option.
EXPLAIN SELECT * FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => Index Scan using idx_book_catalog_isbn -- no full scan needed
                                    -- => cost drops by roughly two orders of magnitude vs the Seq Scan above
