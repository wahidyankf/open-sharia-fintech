-- Example 25: ANALYZE Refresh Stats.
-- The planner's row-count ESTIMATES come from statistics gathered by ANALYZE
-- (co-25) -- a table with NO stats yet gets a generic guess, not a data-aware one.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL, published_year INTEGER NOT NULL);
INSERT INTO book_catalog(id, isbn, price, published_year)
SELECT n, 'ISBN-' || LPAD(n::TEXT, 9, '0'), (10 + (n % 90))::NUMERIC, 2000 + (n % 25)
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 rows -- every isbn value is UNIQUE (1 row each)

-- BEFORE ANALYZE (co-25): no column statistics exist yet for this brand-new data,
-- so the planner falls back to a generic, NOT data-aware selectivity guess.
EXPLAIN SELECT * FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => rows=364 estimated -- a generic guess, badly wrong
                                    -- => (the true answer is exactly 1 row -- isbn is unique)

-- ANALYZE (co-25) samples the table and records real statistics: distinct value
-- counts, most-common values, and a histogram -- the planner now has real data.
ANALYZE book_catalog;

-- AFTER ANALYZE: the SAME query, same plan shape, but a far more accurate estimate.
EXPLAIN SELECT * FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => rows=1 estimated -- ANALYZE learned isbn has ~100,000
                                    -- => distinct values, so 1 row per exact match is now the estimate
