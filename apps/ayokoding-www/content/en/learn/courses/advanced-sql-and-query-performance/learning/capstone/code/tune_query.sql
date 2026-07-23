-- Capstone: tune_query.sql -- the SAME lookup, EXPLAIN ANALYZEd before and after adding
-- the right index (co-18, co-23, co-24). sale_ref matches exactly ONE row out of 250,000
-- (seed.sql), so this is the same "needle in a haystack" shape Example 24 taught, now
-- measured with real ANALYZE timings (PG 18 shows Buffers by default) instead of just
-- EXPLAIN's static estimate.
SET client_min_messages TO WARNING;

-- BEFORE: no index on sale_ref -- the planner's ONLY option is to check every row. On
-- a table this size the planner adds a parallel worker (Gather + Parallel Seq Scan) --
-- still a full scan, just split across 2 workers instead of 1.
EXPLAIN (ANALYZE, BUFFERS) SELECT amount, employee_id, sale_date
FROM sales_event
WHERE sale_ref = 'SALE-000125000';
-- => Gather -> Parallel Seq Scan on sales_event -- Rows Removed by Filter sums to
-- => 249,999 across both workers, real actual time in the single-digit milliseconds --
-- => every one of the 250,000 rows gets read and checked, just split across 2 workers

-- Refresh planner statistics BEFORE measuring "after" too (co-25) -- a fair comparison
-- means BOTH sides ran with current, not stale, statistics.
CREATE INDEX idx_sales_event_sale_ref ON sales_event (sale_ref);

ANALYZE sales_event;
-- => co-25 -- the planner now knows both the new index AND the table's current shape

-- AFTER: the SAME query, unchanged -- only the schema changed.
EXPLAIN (ANALYZE, BUFFERS) SELECT amount, employee_id, sale_date
FROM sales_event
WHERE sale_ref = 'SALE-000125000';
-- => Index Scan using idx_sales_event_sale_ref -- Rows Removed by Filter: 0, real actual
-- => time drops by roughly two orders of magnitude vs the Seq Scan above (co-24)
