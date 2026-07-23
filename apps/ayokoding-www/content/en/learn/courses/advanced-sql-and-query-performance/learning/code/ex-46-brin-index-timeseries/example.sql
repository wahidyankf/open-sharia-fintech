-- Example 46: BRIN Index on Timeseries.
-- BRIN (co-20, Block Range INdex) stores only a MIN/MAX summary per block RANGE,
-- not one entry per row -- tiny on disk, and effective specifically when a column's
-- values correlate with physical insertion order (append-only timestamps, exactly).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS event_log CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE event_log(id INTEGER PRIMARY KEY, occurred_at TIMESTAMP NOT NULL);
                                    -- => occurred_at increases MONOTONICALLY with id -- append-only pattern
INSERT INTO event_log(id, occurred_at)
SELECT n, TIMESTAMP '2026-01-01 00:00:00' + (n || ' seconds')::INTERVAL
FROM generate_series(1, 500000) AS n;
                                    -- => 500,000 rows -- one every second, strictly increasing timestamps

-- CREATE INDEX ... USING brin (co-20) summarizes each block RANGE (many pages) with
-- just a min/max -- orders of magnitude smaller than a B-tree over the same column.
CREATE INDEX idx_event_log_brin ON event_log USING brin (occurred_at);
CREATE INDEX idx_event_log_btree ON event_log USING btree (occurred_at);
                                    -- => a B-tree over the SAME column, for a direct size comparison ONLY
ANALYZE event_log;

SELECT
    pg_size_pretty(pg_relation_size('idx_event_log_brin'))  AS brin_size,
    pg_size_pretty(pg_relation_size('idx_event_log_btree')) AS btree_size;
                                    -- => brin_size is dramatically smaller -- it stores block SUMMARIES, not rows

-- Drop the competing B-tree so the plan below is forced to show BRIN's OWN
-- behavior, not the planner simply preferring the (also valid) B-tree instead.
DROP INDEX idx_event_log_btree;

-- A range predicate on the correlated column uses BRIN effectively -- it scans
-- only the block RANGES whose min/max summary overlaps the requested window.
EXPLAIN SELECT COUNT(*) FROM event_log
WHERE occurred_at BETWEEN '2026-01-02 00:00:00' AND '2026-01-02 01:00:00';
                                    -- => Bitmap Heap Scan + Bitmap Index Scan on idx_event_log_brin
