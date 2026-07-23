-- Example 84: Bulk Load, COPY vs INSERT.
-- COPY (co-28) streams rows in PostgreSQL's own binary/text wire protocol, bypassing
-- the per-statement parse/plan/execute cycle that EVERY individual INSERT pays --
-- for bulk loading, the difference is substantial even at a modest 100,000-row scale.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS bulk_target_insert, bulk_target_copy CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Two IDENTICAL target tables -- one per loading approach -- so the row-by-row
-- INSERT and the COPY below are loading the exact same shape of data.
CREATE TABLE bulk_target_insert(id INTEGER PRIMARY KEY, label TEXT NOT NULL, value NUMERIC(10,2) NOT NULL);
CREATE TABLE bulk_target_copy(id INTEGER PRIMARY KEY, label TEXT NOT NULL, value NUMERIC(10,2) NOT NULL);

-- Generate 100,000 rows of source data to a server-side CSV file (NOT timed --
-- this is test setup, not part of either loading approach being measured).
COPY (
    SELECT n, 'row-' || n, (10 + (n % 90))::NUMERIC FROM generate_series(1, 100000) AS n
) TO '/tmp/bulk_load_data.csv' WITH (FORMAT csv);

\timing on
-- Row-by-row INSERT (co-28): the SAME 100,000 rows, but as 100,000 SEPARATE
-- statement executions -- each one individually parsed, planned, and executed,
-- exactly like an application looping "INSERT one row" per iteration would.
-- A PL/pgSQL DO block loop simulates this worst-case pattern inside a single
-- psql session -- a real offending application would issue these as 100,000
-- separate network round trips, making the real-world cost even higher.
DO $$
DECLARE i INTEGER;
BEGIN
    FOR i IN 1..100000 LOOP
        INSERT INTO bulk_target_insert(id, label, value) VALUES (i, 'row-' || i, (10 + (i % 90))::NUMERIC);
    END LOOP;
END $$;

-- COPY (co-28): the SAME 100,000 rows, streamed from the CSV file as ONE bulk
-- operation -- PostgreSQL parses the format ONCE and appends rows directly.
-- No individual statement parsing/planning per row -- COPY's format is
-- purpose-built for exactly this bulk-append use case.
COPY bulk_target_copy(id, label, value) FROM '/tmp/bulk_load_data.csv' WITH (FORMAT csv);
\timing off
-- Both target tables end up with the IDENTICAL 100,000 rows -- only the
-- LOADING mechanism and its wall-clock cost differ between the two approaches.
