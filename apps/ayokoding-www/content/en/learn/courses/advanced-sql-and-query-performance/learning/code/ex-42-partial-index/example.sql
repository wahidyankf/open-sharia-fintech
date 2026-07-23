-- Example 42: Partial Index.
-- A partial index (co-21) has a WHERE clause of its own -- it indexes only the
-- rows matching that predicate, staying much smaller than a full-table index when
-- the matching rows are a small minority.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS order_row CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE order_row(id INTEGER PRIMARY KEY, status TEXT NOT NULL);
                                    -- => status: mostly 'shipped', a small minority still 'pending'
INSERT INTO order_row(id, status)
SELECT n, CASE WHEN n % 100 = 0 THEN 'pending' ELSE 'shipped' END
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 rows; only 1% (1,000 rows) are 'pending'

-- CREATE INDEX ... WHERE status = 'pending' (co-21) indexes ONLY those 1,000 rows --
-- the other 99,000 'shipped' rows never enter this index at all.
CREATE INDEX idx_order_pending ON order_row(id) WHERE status = 'pending';
ANALYZE order_row;

-- pg_relation_size (a real byte count, not an estimate) proves the partial index is
-- dramatically smaller than a full index over the same 100,000 rows would be.
CREATE INDEX idx_order_full ON order_row(id);
                                    -- => a full, unfiltered index for direct size comparison below
SELECT
    pg_size_pretty(pg_relation_size('idx_order_pending')) AS partial_index_size,
    pg_size_pretty(pg_relation_size('idx_order_full'))    AS full_index_size;
                                    -- => partial_index_size is roughly 1% the size of full_index_size

-- A query whose WHERE clause matches the partial index's own predicate CAN use it.
EXPLAIN SELECT id FROM order_row WHERE status = 'pending';
                                    -- => Index Only Scan using idx_order_pending -- the small, matching index
