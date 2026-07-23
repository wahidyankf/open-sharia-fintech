-- Example 72: Partition Pruning, EXPLAIN.
-- When a query's WHERE clause matches the partition key, the planner can rule OUT
-- entire partitions BEFORE execution (co-28) -- EXPLAIN shows only the relevant
-- partition scanned, not all of them, even though the query names the parent table.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale_event CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Same three-partition setup as Example 71 -- this example reuses that exact
-- schema and data to isolate PRUNING as the one new concept being taught.
CREATE TABLE sale_event(id INTEGER NOT NULL, sale_date DATE NOT NULL, amount NUMERIC(10,2) NOT NULL)
    PARTITION BY RANGE (sale_date);
CREATE TABLE sale_event_2026_01 PARTITION OF sale_event
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE sale_event_2026_02 PARTITION OF sale_event
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE sale_event_2026_03 PARTITION OF sale_event
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
INSERT INTO sale_event(id, sale_date, amount)
SELECT n, '2026-01-01'::DATE + ((n % 90) || ' days')::INTERVAL, (10 + (n % 90))::NUMERIC
FROM generate_series(1, 9000) AS n;
-- ANALYZE gives the planner the row-count statistics it needs to CONFIRM
-- pruning is safe -- without it, the planner can still prune based on the
-- partition bounds alone, but accurate row estimates need fresh statistics.
ANALYZE sale_event;

-- The query below ONLY asks about February -- the planner should rule out
-- January and March ENTIRELY, without scanning a single row from either.
EXPLAIN SELECT * FROM sale_event WHERE sale_date >= '2026-02-01' AND sale_date < '2026-03-01';
                                    -- => "Seq Scan on sale_event_2026_02" ONLY -- no mention at ALL
                                    -- => of sale_event_2026_01 or sale_event_2026_03 in the plan --
                                    -- => partition pruning (co-28) eliminated them before execution
-- Pruning happens at PLAN time here because the WHERE bounds are constant
-- literals -- pruning based on a bind parameter's value happens at EXECUTE
-- time instead, which EXPLAIN ANALYZE (not plain EXPLAIN) would reveal.
