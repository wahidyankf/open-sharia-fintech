-- Example 71: Partition by Range.
-- Declarative range partitioning (co-28) splits ONE logical table into several
-- physical tables by a key range -- PostgreSQL routes each INSERT to the right
-- partition automatically, and each partition can be managed independently.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale_event CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- PARTITION BY RANGE declares the STRATEGY and the KEY column up front -- no
-- partition exists yet until the CREATE TABLE ... PARTITION OF statements below.
CREATE TABLE sale_event(id INTEGER NOT NULL, sale_date DATE NOT NULL, amount NUMERIC(10,2) NOT NULL)
    PARTITION BY RANGE (sale_date);
                                    -- => the PARENT table (co-28) -- holds NO data of its own;
                                    -- => every row physically lives in exactly ONE partition below

-- Each PARTITION OF clause defines a HALF-OPEN range [FROM, TO) -- January's
-- upper bound (2026-02-01) is EXCLUSIVE, matching February's lower bound
-- exactly, so every possible sale_date has exactly one home with no gaps or overlaps.
CREATE TABLE sale_event_2026_01 PARTITION OF sale_event
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE sale_event_2026_02 PARTITION OF sale_event
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE sale_event_2026_03 PARTITION OF sale_event
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
                                    -- => 3 monthly partitions -- each is an ORDINARY table underneath

-- The application INSERTs into the PARENT table name (sale_event) -- it never
-- needs to know which physical partition a given sale_date belongs to.
INSERT INTO sale_event(id, sale_date, amount)
SELECT n, '2026-01-01'::DATE + ((n % 90) || ' days')::INTERVAL, (10 + (n % 90))::NUMERIC
FROM generate_series(1, 9000) AS n;
                                    -- => 9,000 rows spanning all 3 months -- PostgreSQL ROUTES each
                                    -- => row to its matching partition automatically, no manual targeting

-- tableoid is a hidden system column present on every table -- casting it to
-- ::regclass turns the raw OID into its human-readable table name.
SELECT tableoid::regclass AS physical_partition, COUNT(*) AS row_count
FROM sale_event
GROUP BY tableoid
ORDER BY physical_partition;
                                    -- => tableoid (co-28) reveals which PHYSICAL table each row
                                    -- => actually landed in -- confirms the routing worked correctly
-- A query filtering WHERE sale_date falls entirely within one month can also
-- use PARTITION PRUNING to skip scanning the other two partitions entirely.
