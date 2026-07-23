-- Example 22: EXPLAIN Basic.
-- EXPLAIN (co-23) prints the query PLAN the planner chose, without running the
-- query -- estimated row counts and costs only, no actual execution happens.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book_catalog CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE book_catalog(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, price NUMERIC(6,2) NOT NULL, published_year INTEGER NOT NULL);
                                    -- => a wider catalog table, seeded with generated rows below
INSERT INTO book_catalog(id, isbn, price, published_year)
SELECT
    n,
    'ISBN-' || LPAD(n::TEXT, 9, '0'),
    (10 + (n % 90))::NUMERIC,
    2000 + (n % 25)
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 rows -- large enough for the planner to prefer a
                                    -- => sequential scan for most queries with no matching index

-- EXPLAIN (co-23) with no options shows only the ESTIMATED plan -- "cost=..." is
-- an abstract planner unit, "rows=..." is the planner's row-count ESTIMATE.
-- No ANALYZE keyword here -- plain EXPLAIN never executes the query, so
-- there is no actual row/timing data, only the planner's estimates.
EXPLAIN SELECT * FROM book_catalog WHERE isbn = 'ISBN-000050000';
                                    -- => Seq Scan node -- no index exists on isbn yet
                                    -- => Filter: (isbn = 'ISBN-000050000'::text) -- the predicate applied per row
