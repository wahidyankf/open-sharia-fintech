-- Example 73: Partition vs Index, Bulk-Delete Tradeoff.
-- Deleting an old month of data means two very different costs depending on the
-- schema: on a single big table with one big index (co-22), every matching row AND
-- its index entries must be individually removed; on a partitioned table (co-28),
-- dropping the whole partition is a single metadata operation, regardless of size.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale_event_big, sale_event_part CASCADE;
                                    -- => resets state -- this example is fully self-contained

-- Approach A: one big table, one big B-tree index.
-- Both approaches seed the SAME 300,000 rows across the SAME 6-month date
-- range -- only the schema shape differs, isolating that as the one variable.
CREATE TABLE sale_event_big(id INTEGER PRIMARY KEY, sale_date DATE NOT NULL, amount NUMERIC(10,2) NOT NULL);
INSERT INTO sale_event_big(id, sale_date, amount)
SELECT n, '2026-01-01'::DATE + ((n % 180) || ' days')::INTERVAL, (10 + (n % 90))::NUMERIC
FROM generate_series(1, 300000) AS n;
-- This index accelerates lookups AND is exactly what the DELETE below
-- must also update as each matching row is removed.
CREATE INDEX idx_sale_event_big_date ON sale_event_big(sale_date);
ANALYZE sale_event_big;

-- Approach B: range-partitioned by month, each partition gets its OWN local index
-- (created automatically on every partition when you index the PARENT table).
-- Six monthly partitions cover the exact same 6-month span as the big table --
-- January's partition is the one that gets dropped below.
CREATE TABLE sale_event_part(id INTEGER NOT NULL, sale_date DATE NOT NULL, amount NUMERIC(10,2) NOT NULL)
    PARTITION BY RANGE (sale_date);
CREATE TABLE sale_event_part_2026_01 PARTITION OF sale_event_part FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE sale_event_part_2026_02 PARTITION OF sale_event_part FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE sale_event_part_2026_03 PARTITION OF sale_event_part FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE sale_event_part_2026_04 PARTITION OF sale_event_part FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE sale_event_part_2026_05 PARTITION OF sale_event_part FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE sale_event_part_2026_06 PARTITION OF sale_event_part FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
INSERT INTO sale_event_part(id, sale_date, amount)
SELECT n, '2026-01-01'::DATE + ((n % 180) || ' days')::INTERVAL, (10 + (n % 90))::NUMERIC
FROM generate_series(1, 300000) AS n;
CREATE INDEX idx_sale_event_part_date ON sale_event_part(sale_date);
                                    -- => creates a LOCAL index on EACH of the 6 partitions, not one big index
ANALYZE sale_event_part;

-- \timing on turns on psql's built-in wall-clock timer -- the difference below
-- is not hypothetical, it is a real, measurable elapsed-time comparison.
\timing on
-- "Archive off January": DELETE every row matching the month, on the BIG table --
-- every matching heap row AND its index entry must be visited and removed.
-- This DELETE must scan (via the index) roughly 50,000 rows, then individually
-- remove each one from BOTH the heap and the B-tree index structure.
DELETE FROM sale_event_big WHERE sale_date >= '2026-01-01' AND sale_date < '2026-02-01';

-- The SAME logical operation on the partitioned table: drop the partition itself.
-- Its data AND its local index vanish together -- no row-by-row work at all.
-- DROP TABLE on a partition is a metadata-only operation -- its cost does NOT
-- depend on how many rows the partition holds, unlike the DELETE above.
DROP TABLE sale_event_part_2026_01;
\timing off
