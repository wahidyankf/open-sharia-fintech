-- Example 28: psql \timing.
-- \timing (co-23) is a psql meta-command: once turned on, EVERY statement's wall-clock
-- duration prints after its result -- a quick way to compare two queries' actual speed.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- book_catalog is deliberately large (100,000 generated rows) -- \timing's value
-- only becomes visible once a query takes long enough to produce a meaningful duration.
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL);
INSERT INTO book_catalog(id, isbn, price)
SELECT n, 'ISBN-' || LPAD(n::TEXT, 9, '0'), (10 + (n % 90))::NUMERIC
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 rows -- large enough for a measurable duration
                                    -- => \timing measures CLIENT-side wall-clock round-trip time -- it includes
                                    -- => network latency and psql's own result-rendering overhead, not just server-
                                    -- => side execution (contrast Example 23's EXPLAIN ANALYZE, server-side only).

\timing on
                                    -- => turns timing on -- every statement below now reports its duration
-- No index exists yet on book_catalog.price, so this predicate forces a full
-- sequential scan of all 100,000 rows (Example 24 revisits this contrast).
SELECT COUNT(*) FROM book_catalog WHERE price > 50;
                                    -- => the count itself is the query result; \timing adds a "Time:" line
\timing off
                                    -- => turns timing back off -- later statements go back to silent
