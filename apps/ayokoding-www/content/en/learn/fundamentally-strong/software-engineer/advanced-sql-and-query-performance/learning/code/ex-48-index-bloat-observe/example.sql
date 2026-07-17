-- Example 48: Index Bloat, Observed.
-- Every UPDATE creates a NEW index entry (MVCC keeps the old row version alive
-- until nothing can see it, co-22) -- repeatedly updating the SAME rows bloats the
-- index with entries pointing at now-dead row versions, until a VACUUM/REINDEX cleans it up.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS counter_row CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- A single indexed INTEGER column is the whole setup -- deliberately simple so
-- the ONLY thing changing across this script is index size, not query shape.
CREATE TABLE counter_row(id INTEGER PRIMARY KEY, value INTEGER NOT NULL);
INSERT INTO counter_row(id, value)
SELECT n, 0 FROM generate_series(1, 20000) AS n;
                                    -- => 20,000 rows -- these SAME rows get updated repeatedly below
CREATE INDEX idx_counter_value ON counter_row(value);
ANALYZE counter_row;

SELECT pg_size_pretty(pg_relation_size('idx_counter_value')) AS index_size_before;
                                    -- => a small, freshly-built index

-- 20 rounds of updating EVERY row (co-22): each UPDATE leaves the old index entry
-- as dead weight until vacuumed -- 20 x 20,000 = 400,000 dead entries accumulate.
-- PL/pgSQL's DO block runs an anonymous, one-off procedural loop -- there is no
-- plain-SQL way to repeat an UPDATE statement N times without either a loop
-- construct like this or N separate statements.
DO $$
BEGIN
    FOR i IN 1..20 LOOP
        UPDATE counter_row SET value = value + 1;
    END LOOP;
END $$;

SELECT pg_size_pretty(pg_relation_size('idx_counter_value')) AS index_size_bloated;
                                    -- => substantially larger -- dead entries from 20 rounds of updates

-- REINDEX (co-22) rebuilds the index from scratch, containing ONLY live entries --
-- every dead entry from the update churn above is discarded in the rebuild.
-- REINDEX takes an exclusive lock on the index for its duration (Postgres 12+
-- offers REINDEX CONCURRENTLY to avoid that, at the cost of more total work) --
-- acceptable here in a single-writer teaching script, riskier on a live table.
REINDEX INDEX idx_counter_value;

SELECT pg_size_pretty(pg_relation_size('idx_counter_value')) AS index_size_after_reindex;
                                    -- => back down close to the original "before" size
