-- Example 41: Covering Index and Index Only Scan.
-- INCLUDE adds EXTRA columns to an index WITHOUT making them part of the sort key
-- (co-19) -- purely so the index alone can answer a query, letting the planner
-- skip the heap (the actual table storage) entirely: an Index Only Scan (co-24).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL);
INSERT INTO book_catalog(id, isbn, price)
SELECT n, 'ISBN-' || LPAD(n::TEXT, 9, '0'), (10 + (n % 90))::NUMERIC
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 rows -- large enough for the plan choice to matter

-- INCLUDE (price) (co-19) stores price ALONGSIDE the isbn index entries -- price is
-- NOT part of the sort key, just carried along for queries that only need to READ it.
CREATE INDEX idx_book_catalog_isbn_covering ON book_catalog(isbn) INCLUDE (price);
ANALYZE book_catalog;
                                    -- => VACUUM sets the visibility map so Index Only Scan can trust it
VACUUM book_catalog;

-- This query needs ONLY isbn (in WHERE) and price (in SELECT) -- both are present
-- IN the index itself, so EXPLAIN ANALYZE's "Heap Fetches" line proves the heap
-- was never touched at all (co-24) -- the definitive evidence, not just the node name.
EXPLAIN (ANALYZE) SELECT price FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => Index Only Scan using idx_book_catalog_isbn_covering
                                    -- => Heap Fetches: 0 -- the DEFINITIVE proof the heap was skipped
