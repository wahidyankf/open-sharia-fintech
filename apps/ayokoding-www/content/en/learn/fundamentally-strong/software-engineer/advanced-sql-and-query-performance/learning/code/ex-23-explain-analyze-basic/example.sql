-- Example 23: EXPLAIN ANALYZE Basic.
-- EXPLAIN ANALYZE (co-23) actually RUNS the query and reports REAL numbers
-- alongside the estimates -- "actual time", "actual rows" -- plus, new in
-- PostgreSQL 18, buffer hit/read counts print BY DEFAULT (no BUFFERS option needed).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL, published_year INTEGER NOT NULL);
INSERT INTO book_catalog(id, isbn, price, published_year)
SELECT n, 'ISBN-' || LPAD(n::TEXT, 9, '0'), (10 + (n % 90))::NUMERIC, 2000 + (n % 25)
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 rows -- same catalog shape as Example 22

-- EXPLAIN ANALYZE (co-23) executes the query for real, then reports actual vs
-- estimated side by side -- "rows=364" (estimate) vs "actual rows=1" (reality).
EXPLAIN ANALYZE SELECT * FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => estimate says rows=364, actual rows=1 -- a real mismatch
                                    -- => Buffers: shared hit=... appears BY DEFAULT in PG 18, no
                                    -- => BUFFERS option needed (PG <18 required EXPLAIN (ANALYZE, BUFFERS))
