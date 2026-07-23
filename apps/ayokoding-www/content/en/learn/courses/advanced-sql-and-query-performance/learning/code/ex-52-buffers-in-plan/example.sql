-- Example 52: Buffers in the Plan.
-- "Buffers" (co-23, shown by DEFAULT in PostgreSQL 18's EXPLAIN ANALYZE) reports
-- shared "hit" (found already in the buffer cache) vs "read" (fetched from disk) --
-- the single best signal for whether a query is actually I/O-bound.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL);
INSERT INTO book_catalog(id, isbn, price)
SELECT n, 'ISBN-' || LPAD(n::TEXT, 9, '0'), (10 + (n % 90))::NUMERIC
FROM generate_series(1, 200000) AS n;
                                    -- => 200,000 rows -- large enough that shared_buffers may not hold it all

-- PostgreSQL just wrote these rows, so most pages are ALREADY in the shared
-- buffer cache from the INSERT itself -- expect "shared hit", not "shared read".
EXPLAIN (ANALYZE) SELECT COUNT(*) FROM book_catalog WHERE price > 50;
                                    -- => "Buffers: shared hit=1274" -- every page found already in cache
                                    -- => (PG 18 shows this line automatically -- no BUFFERS option written)
                                    -- => "shared read=N" would appear instead for pages NOT in cache,
                                    -- => e.g. right after a fresh server restart with an empty cache
