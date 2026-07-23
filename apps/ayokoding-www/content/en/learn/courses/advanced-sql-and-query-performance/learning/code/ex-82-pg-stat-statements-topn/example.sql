-- Example 82: pg_stat_statements, Top-N.
-- pg_stat_statements (co-25) is NOT enabled by default -- it requires
-- shared_preload_libraries = 'pg_stat_statements' (a server RESTART) plus
-- CREATE EXTENSION pg_stat_statements. Once on, it tracks EVERY query's aggregate cost.
SET client_min_messages TO WARNING;

-- PREREQUISITE #1 (server-level, done at container startup for this example):
--   shared_preload_libraries = 'pg_stat_statements'   -- requires a RESTART to take effect
-- PREREQUISITE #2 (database-level, done here):
-- IF NOT EXISTS makes this statement safely re-runnable -- CREATE EXTENSION
-- errors on a second attempt without it.
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
                                    -- => without BOTH prerequisites, pg_stat_statements simply
                                    -- => does not exist as a queryable view -- this is NOT automatic

-- A small, uninteresting table -- its SCHEMA is not the point of this example;
-- it exists only to give the workload below something real to query against.
DROP TABLE IF EXISTS metric_row CASCADE;
CREATE TABLE metric_row(id INTEGER PRIMARY KEY, category TEXT NOT NULL, value NUMERIC(10,2) NOT NULL);
INSERT INTO metric_row(id, category, value)
SELECT n, 'cat-' || (n % 20), (10 + (n % 90))::NUMERIC FROM generate_series(1, 100000) AS n;
ANALYZE metric_row;

SELECT pg_stat_statements_reset();
                                    -- => clears prior tracked stats -- reset AFTER setup so only the
                                    -- => WORKLOAD below (not table creation) appears in the ranking

-- A "hot endpoint": the SAME cheap lookup, run 200 times -- pg_stat_statements
-- NORMALIZES literal constants, so all 200 calls collapse into ONE tracked entry.
-- A PL/pgSQL DO block is the simplest way to loop 200 times inside a single
-- psql session -- production code would issue these as 200 separate
-- application-level queries, but the tracked-statistics effect is identical.
DO $$
DECLARE i INTEGER;
BEGIN
    FOR i IN 1..200 LOOP
        PERFORM value FROM metric_row WHERE id = i;
    END LOOP;
END $$;

-- ONE genuinely expensive query, run only ONCE.
-- A self-join with a non-equi <= condition, same O(n^2)-flavored pattern as
-- Example 67 -- deliberately restricted to id < 300 so it finishes quickly
-- while still costing far more per call than the 200 cheap lookups above.
SELECT COUNT(*) FROM metric_row a JOIN metric_row b ON b.id <= a.id AND a.id < 300;

-- THE RANKING (co-25): total_exec_time surfaces the query costing the MOST
-- CUMULATIVE time -- not necessarily the slowest per-call, but the biggest total drain.
-- LEFT(query, 55) truncates each tracked query text for readable console output
-- -- pg_stat_statements stores the FULL normalized SQL, which can be long.
SELECT
    LEFT(query, 55) AS query_prefix,
    calls,
    ROUND(total_exec_time::NUMERIC, 3) AS total_exec_time_ms,
    ROUND(mean_exec_time::NUMERIC, 3) AS mean_exec_time_ms
FROM pg_stat_statements
WHERE query ILIKE 'SELECT%'
ORDER BY total_exec_time DESC
LIMIT 5;
-- Expect the 200x cheap lookup to often OUTRANK the 1x expensive join on
-- total_exec_time -- volume can beat per-call cost, which is exactly why
-- ranking by TOTAL time (not mean time) matters for finding real hot spots.
